from django.contrib.gis.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

from utils import app_constant
from utils import utilities
from location.models import Location

from caching.base import CachingManager, CachingMixin

from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _



AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Data table Account table with all attributes
@python_2_unicode_compatible
class Account(CachingMixin, models.Model):
    # This is user_id and will be the same with id in auth_user table
    # This will be the primary key for the table,
    # OneToOneField for make sure it unique in the database table and same with auth_user table
    # , on_delete=models.CASCADE, default=""

    # db_index is use for optimize searches on the columns, only apply if the column have a
    # statistically larger number of rows

    # unique will be true so to make sure there is no duplicate
    # 2 users can't have the same id

    user = models.OneToOneField(AUTH_USER_MODEL, unique=True, max_length=30,
                                primary_key=True, db_index=True)

    # User display name the user
    # add db_index for optimze search for all display_name
    display_name = models.CharField(max_length=50, db_index=True)

    # nick name for user, will be unique
    nickname = models.CharField(max_length=50, unique=True, blank=True)

    # Day of birth field
    dob = models.DateField(blank=True, null=True, db_index=True)

    # gender will based on app_constant.py, by default, if not choice will be Other
    gender = models.CharField(choices=app_constant.GENDER, default=app_constant.G_OTHER, max_length=6)

    # avatar profile image
    avatar_url = models.TextField(default=utilities.get_default_avatar_url(), null=False, blank=False)

    # wallpaper profile image
    wallpaper_url = models.TextField(default=utilities.get_random_wallpaper(), null=False, blank=False)

    # joined date, default = now if from django.utils.timezone module
    join_date = models.DateField(default=now, blank=True, null=True, db_index=True)

    # last action at time
    last_action = models.DateTimeField(default=now, db_index=True)

    # Location attributes, foreignkey is many-to-one relationship
    location = models.ForeignKey(Location, blank=True, null=True, related_name="location")

    is_sharing_location = models.BooleanField(default=False)

    # User level, for future update
    level = models.PositiveSmallIntegerField(default=0, blank=False)

    # Email of username
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)

    # Followers and connections
    followers = models.ManyToManyField('self', blank=True)
    objects = CachingManager()

    REQUIRED_FIELDS = ['username', 'nickname', ]

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        db_table = "account"

    # override the default save function
    def save(self, force_insert=False, validate=True, clean=True,
             write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, signal_kwargs=None, **kwargs):

        if self.display_name is None or len(self.display_name) == 0:
            self.display_name = self.user.username[0: 6] + "**"
            print(self.display_name)

        if self.nickname is None or len(self.nickname) == 0:
            self.nickname = self.user.username
            print(self.nickname)

        return super(Account, self).save()


# Relationship table, this reference to account user table
# The views will take care the relationship, this is just the table to store from who to who
@python_2_unicode_compatible
class RelationShip(CachingMixin, models.Model):
    # request time for friend
    rel_made_at = models.DateTimeField(default=now, blank=True, null=True)
    # request from user
    from_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_user', unique=False)

    # to user
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_user', unique=False)

    # status of the user, based on RELATIONSHIP from app_constant
    status = models.CharField(choices=app_constant.RELATIONSHIP,
                              default=app_constant.R_FRIEND, max_length=20)
    objects = CachingManager()

    class Meta:
        verbose_name = _('RelationShip')
        verbose_name_plural = _('RelationShips')
        unique_together = ('from_user', 'to_user')
        db_table = "relationship"

    def __str__(self):
        return str(self.from_user) + " and " + str(self.to_user)

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be in relationship with themselves.")
        super(RelationShip, self).save(*args, **kwargs)


# Friend request table
# this is the request friend table
# user will use this to make an accept or deny
@python_2_unicode_compatible
class FriendshipRequest(CachingMixin, models.Model):
    request_made_at = models.DateTimeField(default=now, blank=True, null=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender', unique=False)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver', unique=False)

    message = models.TextField(_('Message'), blank=True, null=True)
    found_user_from = models.CharField(default='Search', max_length=50, null=True, blank=True)
    objects = CachingManager()

    class Meta:
        verbose_name = _('Friendship Request')
        verbose_name_plural = _('Friendship Requests')
        unique_together = ('receiver', 'sender')
        db_table = "friendship_request"

    def __str__(self):
        return "User #%s friendship requested #%s" % (self.sender_id, self.receiver_id)

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.sender == self.receiver:
            raise ValidationError("Users cannot be in relationship with themselves.")
        super(FriendshipRequest, self).save(*args, **kwargs)