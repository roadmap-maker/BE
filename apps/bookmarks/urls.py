from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookmarkListView.as_view(), name='bookmark-list'),
    path('<int:roadmap_id>', views.toggle_bookmark, name='bookmark-toggle'),
    path('status/<int:roadmap_id>', views.check_bookmark_status, name='bookmark-status'),
]