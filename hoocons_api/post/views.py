from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from post.serializers import PostSerializer
from post.models import Post
from account.models import Account

from permissions.permissions import IsAdminOrPostAuthor
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import MultipleObjectsReturned

from django.utils.timezone import now
# Create your views here.


class PostView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = PageNumberPagination
    PageNumberPagination.page_size = 20
    parser_classes = (JSONParser,)

    queryset = Post.objects.order_by('id')
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == "PUT" \
                or self.request.method == "PATCH" \
                or self.request.method == "DELETE":
            self.permission_classes = [IsAuthenticated, IsAdminOrPostAuthor]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(PostView, self).get_permissions()

    # ----------------------------------------------------
    # GET API to return single object of Post
    # ----------------------------------------------------
    # PK is primary key, view user profile,
    def list(self, request, pk=None, *args, **kwargs):
        # cache the account object from request user from database.
        # account is a table name in the database
        if request.user.is_active is False:
            return Response({"message": "user does not exists or inactive"}, status=status.HTTP_404_NOT_FOUND)

        _current_user = self.request.user.account

        # save the time this user do this action
        _current_user.last_action = now()
        _current_user.save()

        # get the account object, with the primary key is None
        # from the models.py
        _user = get_object_or_404(Account, pk=pk)

        _post = get_object_or_404(Post, author_id=_user.user_id)
        print("test", _post)

        # _post = get_object_or_404(Post, author=_user.user_id)
        # print(_post)

        # Create a JSON format from the models.py
        serializer = PostSerializer(_post, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        _current_user = self.request.user.account
        _current_user.last_action_at = now()
        _current_user.save()

        try:
            title = request.data['title']
            text_content = request.data['text_content']


            post = Post(author=_current_user, title=title, text_content=text_content)
            post.save()

            return Response(PostSerializer(post, many=False, context={"request": request}).data, status=200)
        except KeyError:
            return Response({"error": "empty field"}, status=200)


    def update(self, request, pk=None, *args, **kwargs):
        pass

    def partial_update(self, request, pk=None, *args, **kwargs):
        pass

    def destroy(self, request, pk=None, *args, **kwargs):
        pass