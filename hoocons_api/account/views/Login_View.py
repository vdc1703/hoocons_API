from rest_framework.response import Response
from utils.utilities import jwt_response_special_handling
from rest_framework import viewsets, status
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from rest_framework_jwt.settings import api_settings

# Create your views here.

#Specify a custom function to generate the token payload
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


#----------------------------------------------------
# Login API and return a token
# and use the token to perform all other thing
#----------------------------------------------------
class LoginView(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    #GET
    # Return all table in datase
    def list(self, request):
        return Response({"message": "not supported"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    #POST
    def create(self, request):
        if request.data is not None:
            try:
                _username = request.data["username"]
                _pwd = request.data["pwd"]

                # Use authenticate() to verify a set of credentials.
                # It takes credentials as keyword arguments, username and password for the default case,
                # checks them against each authentication backend,
                # and returns a User object if the credentials are valid for a backend.
                # If the credentials aren’t valid for any backend or
                # if a backend raises PermissionDenied, it returns None

                _user = authenticate(username=_username, password=_pwd)

                if _user is not None:
                    if _user.is_active:

                        # query all information of user id from auth_user table, inlucde token columns
                        payload = jwt_payload_handler(_user)

                        # get the token from payload
                        token = jwt_encode_handler(payload)

                        # return json format with token {'token':'....'}
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
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
#----------------------------------------------------
# END Login API
#----------------------------------------------------

