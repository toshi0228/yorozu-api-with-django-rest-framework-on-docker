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

    def patch(self, request):
        """よろずやがリクエストを承認したら,is_approvalをfalseからTrueに変更する"""
        print("上書き処理ーーーーーーーーーーーーーーー")
        print(request.data)

        # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
        yorozu_id = self.request.user.profile.yorozu_id

        # 自分にプランのリクエストが来たデータを取り出す
        # 何回も同じ人にリクエストを送ってしまう人がいるので,firstをつける。
        # またorder_by('-created_at')をつける事で、一番最新のリクエストに対して承認する
        queryset = Review.objects.filter(
            sender_yorozu_id=yorozu_id, receiver_yorozu_id=request.data['receiver_yorozu_id']).first()
        # receiver_yorozu_id=yorozu_id, sender_yorozu_id=request.data['sender_yorozu_id']).order_by('-created_at').first()

        # partial=Trueがあることで、引数dataで渡した値のみが更新されるようになる
        serializer = ReviewSerializer(
            instance=queryset, data=request.data, partial=True)

        if serializer.is_valid():
            # patchで変更しても、saveしないとserializer.dataの値は反映されない
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("reviewの上書き失敗", status=status.HTTP_400_BAD_REQUEST)


class ReviewRetrieveAPIView(views.APIView):
    '''プランページに移動した時に、よろずやのレビューの点数を取得する'''

    def get(self, request, pk):

        recieve_review_list = Review.objects.filter(
            receiver_yorozu_id=pk)
        # レビュがある場合は,true
        if recieve_review_list:
            positive_score = []
            negative_score = []

            for recieve_review in recieve_review_list:
                # trueの場合は、特点を追加する
                if recieve_review.is_positive_score:
                    positive_score.append(recieve_review.is_positive_score)

                if recieve_review.is_negative_score:
                    negative_score.append(recieve_review.is_negative_score)

            return Response({"positive_score": len(positive_score), "negative_score": len(negative_score)}, status=status.HTTP_200_OK)

        return Response({"positive_score": 0, "negative_score": 0}, status=status.HTTP_200_OK)
