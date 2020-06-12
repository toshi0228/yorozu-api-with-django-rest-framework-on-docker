from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Request

from ..serializers.serializer_request import RequestSerializer


class RequestListCreateAPIView(views.APIView):
    """自分宛にプランリクエストをして来てくれたお客さんのリストの表示と作成"""

    # この設定があることで、jwtを持っていないと入れない
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
            yorozu_id = self.request.user.profile.yorozu_id
            # 自分にプランのリクエストが来たデータを取り出す
            # .order_by('-created_at')で、フロント側で配列の最初に、新しいデータが入る
            queryset = Request.objects.filter(
                receiver_yorozu_id=yorozu_id).order_by('-created_at')
            # querysetはリスト(iterable)なので、引数にmany=Trueが必要
            serializer = RequestSerializer(instance=queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("認証なし", status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        # シリアライズしたい時は、引数のデータに値を入れる
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print("登録失敗")
        return Response("登録失敗", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """よろずやがリクエストを承認したら,is_approvalをfalseからTrueに変更する"""
        print(request.data)

        # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
        yorozu_id = self.request.user.profile.yorozu_id
        # 自分にプランのリクエストが来たデータを取り出す
        # 何回も同じ人にリクエストを送ってしまう人がいるので,firstをつける。
        # またorder_by('-created_at')をつける事で、一番最新のリクエストに対して承認する
        queryset = Request.objects.filter(
            receiver_yorozu_id=yorozu_id, sender_yorozu_id=request.data['sender_yorozu_id']).order_by('-created_at').first()

        # partial=Trueがあることで、引数dataで渡した値のみが更新されるようになる
        serializer = RequestSerializer(
            instance=queryset, data=request.data, partial=True)

        if serializer.is_valid():
            # patchで変更しても、saveしないとserializer.dataの値は反映されない
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("プランリクエストの承認失敗", status=status.HTTP_400_BAD_REQUEST)


class MyRequestListAPIView(views.APIView):
    """自分が送信したプランリクエストを取得する"""

    def get(self, request):
        try:
            # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
            yorozu_id = self.request.user.profile.yorozu_id
            # 自分でプランリクエストしたデータを取り出す
            # .order_by('-created_at')で、フロント側で配列の最初に、新しいデータが入る
            queryset = Request.objects.filter(
                sender_yorozu_id=yorozu_id).order_by('-created_at')
            # querysetはリスト(iterable)なので、引数にmany=Trueが必要
            serializer = RequestSerializer(instance=queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("認証なし", status=status.HTTP_401_UNAUTHORIZED)
