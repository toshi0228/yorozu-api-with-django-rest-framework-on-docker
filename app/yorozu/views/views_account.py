from rest_framework import viewsets
from rest_framework import status, views
from ..serializers.serializer_account import AccountSerializer
from ..models import Account


class AccountViewSet(viewsets.ModelViewSet):

    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    # jwtの場合、これは使わなくなるのかな..
    # permission_classes = (IsAuthenticated,)

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # authenticationは認証で、そのトークンがデータベースにあるかどうかを判断
    # permissionは、そのユーザーがログインしてあるユーザかどうか判断
    # プロフィルールなど、他の人に、編集やら削除されないために、pemisttiionをつける
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
