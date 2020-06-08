from rest_framework import views, status
from rest_framework.response import Response
from ..models import Tag
from ..serializers.serializer_tag import TagSerializer


class TagListAPIView(views.APIView):

    def get(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # シリアライズしたい時は、引数のデータに値を入れる
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print("登録失敗")
        return Response("登録失敗", status=status.HTTP_400_BAD_REQUEST)
