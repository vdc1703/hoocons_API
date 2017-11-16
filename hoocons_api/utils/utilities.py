# This file use to define global variable use in the API

from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


from rest_framework import permissions
from rest_framework.permissions import IsAdminUser


class IsAdminOrSelf(IsAdminUser):
    """
    Allow access to admin users or the user himself.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        elif request.user and obj.isinstance(request.user) and obj == request.user:
            return True
        return False


class IsAdminOrProfileOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user and request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class IsAdminOrPostAuthor(permissions.BasePermission):
    """
        Object-level permission to only allow owners of an object to edit it.
        Assumes the model instance has an `owner` attribute.
        """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user and request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.
        return obj.author == request.user.userinfo


class IsAdminOrChannelOwner(permissions.BasePermission):
    """
            Object-level permission to only allow owners of an object to edit it.
            Assumes the model instance has an `owner` attribute.
            """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user and request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user.userinfo


class IsAdminOrChannelAdmin(permissions.BasePermission):
    """
            Object-level permission to only allow owners of an object to edit it.
            Assumes the model instance has an `owner` attribute.
            """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user and request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.owner == request.user.userinfo:
            return True
        # Instance must have an attribute named `owner`.
        return request.user.userinfo in obj.admins


def jwt_response_special_handling(response, user=None):
    if user is None:
        token = response.data.get('token')
        user = __resolve_user(token)

    return response

def __resolve_user(token):
    serializer = VerifyJSONWebTokenSerializer(data={'token': token, })
    serializer.is_valid(raise_exception=True)
    return serializer.object.get('user')

# Default avatar image url.
def get_default_avatar_url():
    return 'http://res.cloudinary.com/dumfykuvl/image/upload/v1493749974/images_lm0sjf.jpg'

# Default wallpaper url.
def get_random_wallpaper():
	return 'http://res.cloudinary.com/dumfykuvl/image/upload/v1493749974/images_lm0sjf.jpg'