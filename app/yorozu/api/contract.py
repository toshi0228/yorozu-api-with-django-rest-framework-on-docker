from rest_framework import views, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from ..models import Contract
from ..models import Plan

from ..serializers.serializer_contract import GetContractSerializer, PostContractSerializer


class ReceiveContractListCreateAPIView(views.APIView):
    """自分のプランを契約してくれたお客さんリストの表示と作成"""

    # この設定があることで、jwtを持っていないと入れない
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        try:
            # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
            yorozu_id = self.request.user.profile.yorozu_id
            # 自分宛に契約のリクエストが来たデータを取り出す
            # .order_by('-created_at')で、フロント側で配列の最初に、新しいデータが入る

            queryset = Contract.objects.filter(
                receiver_yorozu_id=yorozu_id).order_by('-created_at')

            # querysetはリスト(iterable)なので、引数にmany=Trueが必要
            serializer = GetContractSerializer(instance=queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("失敗", status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        # シリアライズしたい時は、引数のデータに値を入れる
        serializer = PostContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response("登録失敗", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """よろずやがリクエストを承認したら,is_approvalをfalseからTrueに変更する"""

        # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
        yorozu_id = self.request.user.profile.yorozu_id
        # 自分にプランのリクエストが来たデータを取り出す
        # 何回も同じ人にリクエストを送ってしまう人がいるので,firstをつける。
        # またorder_by('-created_at')をつける事で、一番最新のリクエストに対して承認する
        queryset = Contract.objects.filter(
            receiver_yorozu_id=yorozu_id, sender_yorozu_id=request.data['sender_yorozu_id'], contract_plan=request.data['contract_plan']).order_by('-created_at').first()

        # partial=Trueがあることで、引数dataで渡した値のみが更新されるようになる
        serializer = PostContractSerializer(
            instance=queryset, data=request.data, partial=True)

        if serializer.is_valid():
            # patchで変更しても、saveしないとserializer.dataの値は反映されない
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("プランリクエストの承認失敗", status=status.HTTP_400_BAD_REQUEST)


class MySentContractListAPIView(views.APIView):
    """自分が送信したプラン契約の申請(本契約)を取得する"""

    def get(self, request):
        try:
            # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
            yorozu_id = self.request.user.profile.yorozu_id
            # 自分でプランリクエストしたデータを取り出す
            # .order_by('-created_at')で、フロント側で配列の最初に、新しいデータが入る
            queryset = Contract.objects.filter(
                sender_yorozu_id=yorozu_id).order_by('-created_at')
            # querysetはリスト(iterable)なので、引数にmany=Trueが必要
            serializer = GetContractSerializer(instance=queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("認証なし", status=status.HTTP_401_UNAUTHORIZED)
