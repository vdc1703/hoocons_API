"""hoocons_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from account.views.register_view import RegisterView
from account.views.login_view import LoginView
from account.views.user_view import UserView
from account.views.friend_request_view import FriendRequestView

router = DefaultRouter()
router.register(r'register', RegisterView, base_name='register')
router.register(r'login', LoginView, base_name='auth')
router.register(r'user', UserView, base_name='user')
router.register(r'friend/request', FriendRequestView, base_name='fr_request')

urlpatterns = [
    url(r'^/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]
