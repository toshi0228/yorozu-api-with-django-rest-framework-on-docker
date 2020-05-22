from rest_framework import views, status
from rest_framework.response import Response
from ..models import Tag
from ..serializers.serializer_tag import TagSerializer


class TagListAPIView(views.APIView):

    def get(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class TagViewSet(viewsets.ModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
