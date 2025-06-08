from rest_framework import serializers
from .models import Bookmark
from apps.roadmaps.serializers import RoadmapListSerializer


class BookmarkSerializer(serializers.ModelSerializer):
    roadmap = RoadmapListSerializer(read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['id', 'roadmap', 'created_at']
        read_only_fields = ['id', 'created_at']


class BookmarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['roadmap']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_roadmap(self, value):
        user = self.context['request'].user
        # 이미 북마크한 로드맵인지 확인
        if Bookmark.objects.filter(user=user, roadmap=value).exists():
            raise serializers.ValidationError("이미 북마크한 로드맵입니다.")
        return value