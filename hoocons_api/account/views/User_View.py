from django.contrib.auth.models import User
from rest_framework.response import Response
from django.db.models import Q

# REST_Framework
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework_jwt.settings import api_settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from account.models import Account, RelationShip

from utils.utilities import IsAdminOrProfileOwner
from utils import app_constant
from account.serializer import AccountSerializer

# Create your views here.

#Specify a custom function to generate the token payload
# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

class UserView(viewsets.ModelViewSet):
	authentication_classes = (JSONWebTokenAuthentication,)
	pagination_class = PageNumberPagination
	PageNumberPagination.page_size = 20
	parser_classes = (JSONParser,)

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

	# PK is primary key, view user profile,
	def retrieve(self, request, pk=None, *args, **kwargs):
		# cache the account object from request user
		_current_user = self.request.user.account

		# save the time this user do this action
		_current_user.last_action = now()
		_current_user.save()

		# get the account object, with the primary key is None
		_user = get_object_or_404(Account, pk=pk)

		# to make sure the user who view the profile is not in block list and the user have to be active
		if self.is_blocked(_current_user, _user):
			return Response({"message": "user does not exists or inactive"}, status=status.HTTP_404_NOT_FOUND)
		elif _user.user.is_active is False:
			return Response({"message": "user does not exists or inactive"}, status=status.HTTP_404_NOT_FOUND)

		serializer = self.get_serializer(_user, many=False, context={"request": request})

		return Response(serializer.data, status=status.HTTP_200_OK)


	def is_blocked(self, request_user, user):
		if RelationShip.objects.filter(Q(from_user=request_user, to_user=user) |
										   Q(from_user=user, to_user=request_user),
										   status=app_constant.R_BLOCKED).exists():
			return True
		return False