from rest_framework import viewsets
from ..models import Tag
from ..serializers.serializer_tag import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
