# This User_View is use to view the user profile

from rest_framework.response import Response
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.gis.geos import Point

# REST_Framework
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route, detail_route

from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from account.models import Account, RelationShip, FriendshipRequest
from location.models import Location
from permissions.permissions import IsAdminOrProfileOwner

from utils.utilities import is_valid_coordinate
from utils import app_constant
from account.serializer import AccountSerializer

# Create your views here.

#----------------------------------------------------
# UserView API, return User information
#----------------------------------------------------
class UserView(viewsets.ModelViewSet):
	authentication_classes = (JSONWebTokenAuthentication,)
	pagination_class = PageNumberPagination
	PageNumberPagination.page_size = 20
	parser_classes = (JSONParser,)

	queryset = Account.objects.all()
	serializer_class = AccountSerializer

	# permission for see the UserView, must use token
	def get_permissions(self):
		if self.request.method == "PUT" \
				or self.request.method == "PATCH" \
				or self.request.method == "DELETE":
			self.permission_classes = [IsAuthenticated, IsAdminOrProfileOwner]
		else:
			self.permission_classes = [IsAuthenticated, ]
		return super(UserView, self).get_permissions()

	# ----------------------------------------------------
	# GET API to return single object profile of user
	# ----------------------------------------------------
	# PK is primary key, view user profile,
	def retrieve(self, request, pk=None, *args, **kwargs):
		# cache the account object from request user from database.
		# account is a table name in the database
		_current_user = self.request.user.account

		# save the time this user do this action
		_current_user.last_action = now()
		_current_user.save()

		# get the account object, with the primary key is None
		# from the models.py
		_user = get_object_or_404(Account, pk=pk)



		# to make sure the user who view the profile is not in block list and the user have to be active
		if self.is_blocked(_current_user, _user):
			return Response({"message": "user does not exists or inactive"}, status=status.HTTP_404_NOT_FOUND)
		# check in auth_user table is the user is_active or not
		elif _user.user.is_active is False:
			return Response({"message": "user does not exists or inactive"}, status=status.HTTP_404_NOT_FOUND)

		# Create a JSON format from the models.py
		serializer = self.get_serializer(_user, many=False, context={"request": request})
		return Response(serializer.data, status=status.HTTP_200_OK)

	#----------------------------------------------------
	# Update API for user after register
	#----------------------------------------------------
	def update(self, request, pk=None, *args, **kwargs):

		# Get the user account object based on the token
		_target_user = get_object_or_404(Account, pk=pk)

		# Check permission
		self.check_object_permissions(request, _target_user)

		# Check if the user if active or banned
		if request.user.is_active is False:
			return Response({"message": "user is inactive or banned"}, status=status.HTTP_423_LOCKED)

		_target_user.last_action_at = now()


		if request.data is not None:
			try:
				# get gender, required field.
				gender = request.data['gender']
				if gender is not None and len(gender) > 0:
					_target_user.gender = gender

				# get display_name, optional
				try:
					display_name = request.data['display_name']
					if display_name is not None and len(display_name) > 0:
						_target_user.display_name = display_name
				except KeyError:
					pass

				# get nickname, optional
				try:
					nickname = request.data['nickname']
					if nickname is not None and len(nickname) > 0:
						_target_user.nickname = nickname
				except KeyError:
					pass

				# get day of birth, optional
				try:
					birthday = request.data['dob']
					if birthday is not None and len(birthday) > 0:
						_target_user.dob = birthday
				except KeyError:
					pass

				# try:
				# 	work = request.data['work']
				# 	_target_user.work = work
				# except KeyError:
				# 	pass

				# try:
				# 	profile_media = request.data['profile_media']
				# 	serializer = MediaSerializer(profile_media, many=False)
				# 	if serializer.data is not None:
				# 		media = Media.objects.create(url=serializer.data['url'], type=serializer.data['type'])
				# 		_target_user.profile_medias.add(media)
				# 		_target_user.profile_url = serializer.data['url']
				# except KeyError:
				# 	pass

				# try:
				# 	wallpaper_media = request.data['wallpaper_media']
				# 	serializer = MediaSerializer(wallpaper_media, many=False)
				# 	if serializer.data is not None:
				# 		media = Media.objects.create(url=serializer.data['url'], type=serializer.data['type'])
				# 		_target_user.wallpaper_medias.add(media)
				# 		_target_user.wallpaper_url = serializer.data['url']
				# except KeyError:
				# 	pass

				# Try catching location
				try:
					location_name = None
					city = None
					province = None
					state = None
					zipcode = -1
					country = None
					address = None
					place_id = None
					place_api_type = None

					location_json = request.data['location']
					coordinate_json = location_json['coordinate']

					# getting location information
					longitude = float(coordinate_json['longitude'])
					latitude = float(coordinate_json['latitude'])

					try:
						location_name = location_json['location_name']
					except KeyError:
						pass

					try:
						city = location_json['city']
					except KeyError:
						pass

					try:
						province = location_json['province']
					except KeyError:
						pass

					try:
						state = location_json['state']
					except KeyError:
						pass

					try:
						zipcode = int(location_json['zipcode'])
					except KeyError:
						pass

					try:
						country = location_json['country']
					except KeyError:
						pass

					try:
						address = location_json['address']
					except KeyError:
						pass

					try:
						place_id = location_json['place_id']
					except KeyError:
						pass

					try:
						place_api_type = location_json['place_api_type']
					except KeyError:
						pass

					if is_valid_coordinate(longitude=longitude, latitude=latitude):
						coordinate = Point(x=longitude, y=latitude, srid=4326)
						location = Location.objects.create(coordinate=coordinate, location_name=location_name,
														   city=city, province=province, state=state,
														   zipcode=zipcode, country=country, address=address,
														   place_id=place_id, place_api_type=place_api_type)
						_target_user.location = location
						_target_user.last_action = now()
					else:
						return Response({"error": "invalid location"}, status=status.HTTP_206_PARTIAL_CONTENT)
				except KeyError:
					_target_user.coordinate = Point(0, 0, srid=4326)

				_target_user.save()
				return Response({"message": "success"}, status=status.HTTP_200_OK)
			except KeyError:
				return Response({"error": "Missing gender"}, status=status.HTTP_204_NO_CONTENT)
			except IntegrityError as e:
				return Response({"error": str(e)}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
			except AssertionError as e:
				return Response({"error": str(e)}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
			except AttributeError as e:
				return Response({"error": str(e)}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	# ----------------------------------------------------
	# END Update API
	# ----------------------------------------------------

	# Request to make friend
	# Link to call
	# link:/api/view/1/makefriend

	@detail_route(methods=['post', 'delete'])
	def makefriend(self, request, pk=None):

		# cache to user object from PostgresSQl database based on user token
		_current_user = request.user.account

		# Check to make sure user is active
		if _current_user.user.is_active is False:
			return Response({"message": "user is inactive or banned"}, status=status.HTTP_423_LOCKED)

		_current_user.last_action_at = now()
		_current_user.save()

		# Get the Account object from the view link
		# ex: apt/user/2/makefriend, will return user of ID=2
		_user = get_object_or_404(Account, pk=pk)

		# check to make sure both user is not in blocklist from each other
		if self.is_blocked(_current_user, _user):
			return Response({"message": "user does not exists"}, status=status.HTTP_404_NOT_FOUND)
		# and make sure the user is active
		elif _user.user.is_active is False:
			return Response({"message": "user does not exists"}, status=status.HTTP_404_NOT_FOUND)

		# If request using POST method
		# This will create a friend request
		if request.method == "POST":

			# if the user is friend already, return
			if self.is_friend(_current_user, _user):
				return Response({"message": "already friend"}, status=status.HTTP_201_CREATED)

			# # *************************
			# # If this request is already have made from other user
			# try:
			# 	friend_request = FriendshipRequest.objects.get(sender=_user, receiver=_current_user)
			# 	RelationShip.objects.create(from_user=_current_user, to_user=_user,
			# 								status=app_constant.relationship_friend)
			# 	# Create activity object for two users
			# 	Activity.objects.create(actor=_current_user, privacy=app_constant.privacy_private,
			# 							tag=app_constant.action_making_friend, target=friend_request.send_from)
			#
			# 	Activity.objects.create(actor=friend_request.send_from, privacy=app_constant.privacy_private,
			# 							tag=app_constant.action_making_friend, target=_current_user)
			# 	friend_request.delete()
			# 	return Response({"message": "success"}, status=status.HTTP_200_OK)
			# except FriendshipRequest.DoesNotExist:
			# 	pass
			# *************************

			# If this request is already made before
			try:
				FriendshipRequest.objects.get(sender=_current_user, receiver=_user)
				return Response({"message": "request is already made"}, status=status.HTTP_303_SEE_OTHER)
			except FriendshipRequest.DoesNotExist:
				pass

			# *************************
			# Nothing happened before, create a normal request
			try:
				message = request.data["message"]
			except KeyError:
				message = None

			FriendshipRequest.objects.create(sender=_current_user, receiver=_user, message=message)
			return Response({"message": "success"}, status=status.HTTP_200_OK)

		# If request using DELETE method.
		# This will delete friendship
		elif request.method == "DELETE":
			#
			try:
				friendship = RelationShip.objects.get(Q(from_user=_current_user, to_user=_user) |
													  Q(from_user=_user, to_user=_current_user),
													  status=app_constant.R_FRIEND)
				friendship.delete()
				return Response({"message": "unfriend complete"}, status=status.HTTP_200_OK)
			except RelationShip.DoesNotExist:
				return Response({"message": "not friend"}, status=status.HTTP_204_NO_CONTENT)


	# function use to check if the user is in block list or not based on relationship object from database
	def is_blocked(self, request_user, user):
		if RelationShip.objects.filter(Q(from_user=request_user, to_user=user) |
											   Q(from_user=user, to_user=request_user),
									   status=app_constant.R_BLOCKED).exists():
			return True
		return False
	# function use to check if the user is friend or not based on relationship object from database
	def is_friend(self, request_user, user):
		if RelationShip.objects.filter(Q(from_user=request_user, to_user=user) |
											   Q(from_user=user, to_user=request_user),
									   status=app_constant.R_FRIEND).exists():
			return True

		return False
#----------------------------------------------------
# END UserView API
#----------------------------------------------------
