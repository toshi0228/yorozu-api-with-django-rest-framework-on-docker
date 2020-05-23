from rest_framework import status, views
from rest_framework.response import Response
from ..serializers.serializer_account import AccountSerializer
from ..models import Account


# アカウントモデルの詳細(yorozuIDのみ表示)
class AccountRetrieveAPIView(views.APIView):
    def get(self, request, pk):
        queryst = Account.objects.get(id=pk)
        return Response(queryst.profile.yorozu_id, status=status.HTTP_200_OK)


class AccountCreateAPIView(views.APIView):
    def post(self, request):

        serializer = AccountSerializer(data=request.data)
        serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
            return Response({"アカウント作成成功"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AccountViewSet(viewsets.ModelViewSet):

#     serializer_class = AccountSerializer
#     queryset = Account.objects.all()

#     # jwtの場合、これは使わなくなるのかな..
#     # permission_classes = (IsAuthenticated,)

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # authenticationは認証で、そのトークンがデータベースにあるかどうかを判断
    # permissionは、そのユーザーがログインしてあるユーザかどうか判断
    # プロフィルールなど、他の人に、編集やら削除されないために、pemisttiionをつける
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
