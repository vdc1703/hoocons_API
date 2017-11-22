from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from post.serializers import PostSerializer
from post.models import Post
from permissions.permissions import IsAdminOrPostAuthor
from rest_framework.permissions import IsAuthenticated

from django.utils.timezone import now
# Create your views here.


class PostView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = PageNumberPagination
    PageNumberPagination.page_size = 20
    parser_classes = (JSONParser,)

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == "PUT" \
                or self.request.method == "PATCH" \
                or self.request.method == "DELETE":
            self.permission_classes = [IsAuthenticated, IsAdminOrPostAuthor]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(PostView, self).get_permissions()

    def list(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        _current_user = request.user.userinfo
        _current_user.last_action_at = now()
        _current_user.save()

        try:
            title = request.data['title']
            text_content = request.data['text_content']


            post = Post(author=_current_user, title=title, text_content=text_content)
            return Response(PostSerializer(post, many=False, context={"request": request}).data, status=200)
        except KeyError:
            return Response({"error": "empty field"}, status=200)

    def retrieve(self, request, pk=None, *args, **kwargs):
        pass

    def update(self, request, pk=None, *args, **kwargs):
        pass

    def partial_update(self, request, pk=None, *args, **kwargs):
        pass

    def destroy(self, request, pk=None, *args, **kwargs):
        pass