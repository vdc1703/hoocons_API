# This file use to define global variable use in the API

from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


def jwt_response_special_handling(response, user=None):
    if user is None:
        token = response.data.get('token')
        user = __resolve_user(token)

    return response

def __resolve_user(token):
    serializer = VerifyJSONWebTokenSerializer(data={'token': token, })
    serializer.is_valid(raise_exception=True)
    return serializer.object.get('user')


def is_valid_coordinate(longitude, latitude):
    if longitude < -180 or longitude > 180:
        return False
    if latitude < -90 or latitude > 90:
        return False
    return True


# Default avatar image url.
def get_default_avatar_url():
    return 'http://res.cloudinary.com/dumfykuvl/image/upload/v1493749974/images_lm0sjf.jpg'

# Default wallpaper url.
def get_random_wallpaper():
	return 'http://res.cloudinary.com/dumfykuvl/image/upload/v1493749974/images_lm0sjf.jpg'