from rest_framework import views, status
from rest_framework.response import Response
from ..models import Review
from ..serializers.serializer_review import ReviewSerializer

from rest_framework.permissions import IsAuthenticated


class ReviewListAPIView(views.APIView):

    # この設定があることで、jwtを持っていないと入れない
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request)
        # シリアライズしたい時は、引数のデータに値を入れる
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("登録失敗")
        return Response("登録失敗", status=status.HTTP_400_BAD_REQUEST)
