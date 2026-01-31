from .models import Banner
from rest_framework import serializers


class BannerSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    idea = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ['id', 'image', 'title', 'idea', 'link_url']

    def get_title(self, obj):
        return obj.get_title(self.context.get("language", "ru"))
    
    def get_idea(self, obj):
        return obj.get_idea(self.context.get("language", "ru"))


    