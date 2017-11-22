from rest_framework import serializers

from account.serializer import SimpleUserInfoSerializer

from post.models import Post

class PostSerializer(serializers.ModelSerializer):
	author = serializers.SerializerMethodField('attempt_get_author_info')

	def attempt_get_author_info(self, event):
		serializer = SimpleUserInfoSerializer(event.author, many=False,
											  context={'request': self.context.get('request')})
		return serializer.data

	# return format in Json with author, title, text_content
	class Meta:
		model = Post
		fields = ('author', "title", "text_content")