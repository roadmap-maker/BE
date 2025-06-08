from django.urls import path
from . import views

urlpatterns = [
    # Roadmap endpoints
    path('', views.RoadmapListCreateView.as_view(), name='roadmap-list-create'),
    path('<int:pk>', views.RoadmapDetailView.as_view(), name='roadmap-detail'),
    
    # RoadmapNode endpoints
    path('nodes', views.create_roadmap_node, name='roadmap-node-create'),
    path('nodes/<int:node_id>', views.roadmap_node_detail, name='roadmap-node-detail'),
]