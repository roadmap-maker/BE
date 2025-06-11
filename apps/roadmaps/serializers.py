from rest_framework import serializers
from .models import Roadmap, RoadmapNode


class RoadmapNodeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent_id = serializers.IntegerField(source='parent.id', read_only=True, allow_null=True)
    
    class Meta:
        model = RoadmapNode
        fields = ['id', 'parent_id', 'title', 'content', 'x_coord', 'y_coord', 'created_at', 'updated_at', 'children']
        
    def get_children(self, obj):
        children = obj.children.all()
        return RoadmapNodeSerializer(children, many=True).data


class RoadmapListSerializer(serializers.ModelSerializer):
    """목록 조회용 간단한 시리얼라이저 (노드 정보 제외)"""
    author = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Roadmap
        fields = ['id', 'title', 'description', 'author', 'created_at', 'updated_at']


class RoadmapSerializer(serializers.ModelSerializer):
    """상세 조회용 시리얼라이저 (노드 정보 포함)"""
    nodes = serializers.SerializerMethodField()
    author = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Roadmap
        fields = ['id', 'title', 'description', 'author', 'created_at', 'updated_at', 'nodes']
        
    def get_nodes(self, obj):
        # Only get root nodes (nodes without parent)
        root_nodes = obj.nodes.filter(parent=None)
        return RoadmapNodeSerializer(root_nodes, many=True).data


class RoadmapCreateSerializer(serializers.ModelSerializer):
    nodes = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False,
        allow_empty=True
    )
    author = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Roadmap
        fields = ['title', 'description', 'author', 'nodes']
        
    def create(self, validated_data):
        nodes_data = validated_data.pop('nodes', [])
        validated_data['user'] = self.context['request'].user
        roadmap = super().create(validated_data)
        
        # Create nodes recursively if provided
        try:
            self._create_nodes_recursively(roadmap, nodes_data, None)
        except Exception as e:
            roadmap.delete()
            raise serializers.ValidationError({
                'nodes': f"Node creation failed: {str(e)}"
            })
        
        return roadmap
    
    def update(self, instance, validated_data):
        nodes_data = validated_data.pop('nodes', None)
        
        # Update basic roadmap fields
        instance = super().update(instance, validated_data)
        
        # If nodes data is provided, recreate all nodes
        if nodes_data is not None:
            # Delete existing nodes
            instance.nodes.all().delete()
            
            # Create new nodes recursively
            try:
                self._create_nodes_recursively(instance, nodes_data, None)
            except Exception as e:
                raise serializers.ValidationError({
                    'nodes': f"Node update failed: {str(e)}"
                })
        
        return instance
    
    def _create_nodes_recursively(self, roadmap, nodes_data, parent_node):
        """Recursively create nodes and their children"""
        for node_data in nodes_data:
            # Extract children data before creating the node
            children_data = node_data.pop('children', [])
            
            # Prepare node data
            node_create_data = {
                'roadmap': roadmap.id,
                'parent': parent_node.id if parent_node else None,
                'title': node_data.get('title'),
                'content': node_data.get('content', ''),
                'x_coord': node_data.get('x_coord'),
                'y_coord': node_data.get('y_coord')
            }
            
            # Create the node
            node_serializer = RoadmapNodeCreateSerializer(data=node_create_data, context=self.context)
            if node_serializer.is_valid():
                created_node = node_serializer.save()
                
                # Recursively create children
                if children_data:
                    self._create_nodes_recursively(roadmap, children_data, created_node)
            else:
                raise serializers.ValidationError(f"Node validation failed: {node_serializer.errors}")


class RoadmapNodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapNode
        fields = ['roadmap', 'parent', 'title', 'content', 'x_coord', 'y_coord']
        
    def validate_roadmap(self, value):
        # Ensure user can only create nodes for their own roadmaps
        if value.user != self.context['request'].user:
            raise serializers.ValidationError("You can only create nodes for your own roadmaps.")
        return value
        
    def validate_parent(self, value):
        # Ensure parent node belongs to the same roadmap
        if value:
            roadmap_id = self.initial_data.get('roadmap')
            if isinstance(roadmap_id, int):
                # Compare with roadmap ID
                if value.roadmap.id != roadmap_id:
                    raise serializers.ValidationError("Parent node must belong to the same roadmap.")
            else:
                # Compare with roadmap object
                if value.roadmap != roadmap_id:
                    raise serializers.ValidationError("Parent node must belong to the same roadmap.")
        return value