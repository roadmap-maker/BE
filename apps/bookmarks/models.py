from django.db import models
from django.contrib.auth.models import User
from apps.roadmaps.models import Roadmap


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'roadmap')  # 같은 사용자가 같은 로드맵을 중복 북마크할 수 없음
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.roadmap.title}"
