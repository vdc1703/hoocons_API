from django.db import models

from account.models import Account
from location.models import Location

from caching.base import CachingManager, CachingMixin
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


# Create your models here.
# This Post use to store post information from a post
class Post(models.Model):
	author = models.ForeignKey(Account, db_index=True, blank=False,related_name="author_account")
	created_at = models.DateTimeField(default=now, db_index=True)

	# Content of a post
	title = models.CharField(max_length=200, blank=True, null=True)
	text_content = models.TextField(blank=True, null=True)

	# media --- later
	# media = models.ManyToManyField(media, blank=True)

	# location posted/tagged
	posted_at = models.ForeignKey(Location, blank=True, null=True, related_name="posted_location",on_delete=models.CASCADE)
	tagged_at = models.ForeignKey(Location, blank=True, null=True, related_name="tagged_location", on_delete=models.CASCADE)
	contain_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

	# who like the post
	likes = models.ManyToManyField(Account, blank=True, related_name="likes_account")

	objects = CachingManager()

	class Meta:
		verbose_name = _("Post")
		verbose_name_plural = _("Posts")
		db_table = "post"

	# __unicode__ on Python 2
	def __str__(self):
		return self.text_content