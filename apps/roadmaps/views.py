from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Roadmap, RoadmapNode
from .serializers import (
    RoadmapSerializer,
    RoadmapListSerializer,
    RoadmapCreateSerializer,
    RoadmapNodeSerializer,
    RoadmapNodeCreateSerializer
)


class RoadmapListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Roadmap.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RoadmapCreateSerializer
        return RoadmapListSerializer


class RoadmapDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Roadmap.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RoadmapCreateSerializer
        return RoadmapSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_roadmap_node(request):
    serializer = RoadmapNodeCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def roadmap_node_detail(request, node_id):
    node = get_object_or_404(RoadmapNode, id=node_id, roadmap__user=request.user)
    
    if request.method == 'DELETE':
        node.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = RoadmapNodeCreateSerializer(
            node, 
            data=request.data, 
            context={'request': request},
            partial=(request.method == 'PATCH')
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
