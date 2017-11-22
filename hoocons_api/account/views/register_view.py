from django.contrib.auth.models import User
from rest_framework.response import Response
from utils.utilities import jwt_response_special_handling

from rest_framework import viewsets, status
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from rest_framework_jwt.settings import api_settings

from account.models import Account

#Specify a custom function to generate the token payload
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

#----------------------------------------------------
# register API using POST only.
#----------------------------------------------------
class RegisterView(viewsets.ViewSet):

    # this to allow any request, if not it will return
    # {"detail": "Authentication credentials were not provided."}
    # and denied any POST when try to request register API
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    #GET
    # Return all table in database
    def list(self, request, *args, **kwargs):
        return Response({"message": "not supported"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    #POST
    def create(self, request):
        # Make sure the input data is not None
        if request.data is not None:
            try:
                # Get data from request
                _username = request.data["username"]
                _pwd = request.data["pwd"]

                # Create user/password and save in auth_user table
                # if username is duplicate, return Exception Type: IntegrityError
                #
                User.objects.create_user(username=_username,
                                     password=_pwd,
                                     is_staff=False)

                # Use authenticate() to verify a set of credentials.
                # It takes credentials as keyword arguments, username and password for the default case,
                # checks them against each authentication backend,
                # and returns a User object if the credentials are valid for a backend.
                # If the credentials aren’t valid for any backend or
                # if a backend raises PermissionDenied, it returns None

                # basically, this check if the username is in the auth_user, else, it will return None
                _user = authenticate(username=_username, password=_pwd)

                #print(_user)

                if _user is not None:
                    if _user.is_active:
                        #return Response("You are here", status.HTTP_204_NO_CONTENT)

                        #Create Register object, link the ID from auth_user to ID from reigster make it onetoonefield.
                        # All other columns will be blank which value is ""
                        # Those columns will be generated later
                        Account.objects.create(user=_user)
                        # user = Register(username=_username, pwd=_pwd)
                        # user.save()

                        # query all information of user id from auth_user table, inlucde token columns
                        payload = jwt_payload_handler(_user)

                        # get the token from payload
                        token = jwt_encode_handler(payload)

                        #return json format with token {'token':'....'}
                        response_data = jwt_response_payload_handler(token, _user, request)

                        # return user_id
                        response_data['user_id'] = _user.pk

                        # return token with user_id
                        # {"token":"...", "user_id": id}
                        return jwt_response_special_handling(
                            Response(response_data, status.HTTP_201_CREATED), user=_user
                        )

                    else:
                        return Response("This account is not active", status=status.HTTP_423_LOCKED)
                else:
                    return Response("Failed to login", status=status.HTTP_401_UNAUTHORIZED)

            except KeyError:
                return Response({"message": "Invalid content"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except IntegrityError as e:
                return Response(str(e), status.HTTP_409_CONFLICT)
            except AssertionError as e:
                return Response(str(e), status.HTTP_409_CONFLICT)

        # if the data input is None, return bad request
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # if user1 is not None:
        #     user = Register(username=_username, pwd=_pwd)
        #     user.save()
        #     return Response(RegisterSerializer(user, many=False).data, status=200)
        # # else, return error string
        # else:
        #     return Response("user already exist", status.HTTP_204_NO_CONTENT)  # Otherwise, return True

#----------------------------------------------------
#END REGISTER API
#----------------------------------------------------