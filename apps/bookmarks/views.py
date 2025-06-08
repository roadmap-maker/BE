from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Bookmark
from .serializers import BookmarkSerializer
from apps.roadmaps.models import Roadmap


class BookmarkListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_bookmark(request, roadmap_id):
    """로드맵 북마크 토글 (추가/제거)"""
    roadmap = get_object_or_404(Roadmap, id=roadmap_id)
    try:
        bookmark = Bookmark.objects.get(user=request.user, roadmap=roadmap)
        bookmark.delete()
        return Response({'message': '북마크가 제거되었습니다.', 'bookmarked': False})
    except Bookmark.DoesNotExist:
        bookmark = Bookmark.objects.create(user=request.user, roadmap=roadmap)
        serializer = BookmarkSerializer(bookmark)
        return Response({
            'message': '북마크가 추가되었습니다.',
            'bookmarked': True,
            'bookmark': serializer.data
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_bookmark_status(request, roadmap_id):
    """특정 로드맵의 북마크 상태 확인"""
    roadmap = get_object_or_404(Roadmap, id=roadmap_id)
    is_bookmarked = Bookmark.objects.filter(user=request.user, roadmap=roadmap).exists()
    return Response({'bookmarked': is_bookmarked})