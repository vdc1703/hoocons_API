from caching.base import CachingMixin, CachingManager
from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible
from account.models import Account
from utils import app_constant


@python_2_unicode_compatible
class ChatRoom(CachingMixin, models.Model):
    users = models.ManyToManyField(Account, blank=False)
    active_with = models.ManyToManyField(Account, blank=False, related_name="active_with")
    room_type = models.CharField(max_length=20, blank=False, null=False, choices=app_constant.CHATROOM, db_index=True)
    uid = models.CharField(max_length=250, blank=False, null=False)
    objects = CachingManager()

    class Meta:
        db_table = "chatroom"

