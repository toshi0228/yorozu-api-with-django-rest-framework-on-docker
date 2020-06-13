from rest_framework import views, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from ..models import Contract
from ..models import Plan

from ..serializers.serializer_contract import ContractSerializer


class ReceiveContractListCreateAPIView(views.APIView):
    """自分宛に届いたプラン契約してくれたお客さんおリストの表示と作成"""

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
            serializer = ContractSerializer(instance=queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("認証なし", status=status.HTTP_401_UNAUTHORIZED)

    # def post(self, request):
    #     # シリアライズしたい時は、引数のデータに値を入れる
    #     serializer = RequestSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     print("登録失敗")
    #     return Response("登録失敗", status=status.HTTP_400_BAD_REQUEST)
