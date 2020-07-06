from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
# from rest_framework import generics
from ..models import Message
from ..serializers.serializer_message import MessageSerializer


class MessageListCreateAPIView(views.APIView):
    '''自分自身が送信したメッセージの一覧とメッセージ作成APIクラス'''
    # この設定があることで、jwtを持っていないと入れない
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
            yorozu_id = self.request.user.profile.yorozu_id
            # 送信者が自分のメッセージを取り出す
            queryset = Message.objects.filter(sender_yorozu_id=yorozu_id)
            # querysetはリスト(iterable)なので、引数にmany=Trueが必要
            serializer = MessageSerializer(instance=queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("認証なし", status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("登録失敗")
        return Response("登録失敗", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """メッセージの未読を既読にする処理"""

        queryset = Message.objects.get(id=request.data['id'])

        # partial=Trueがあることで、引数dataで渡した値のみが更新されるようになる
        serializer = MessageSerializer(
            instance=queryset, data=request.data, partial=True)

        # is_valid()をしないと、データは取得できない
        if serializer.is_valid():
            # patchで変更しても、saveしないとserializer.dataの値は反映されない
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("メッセージの既読処理の失敗", status=status.HTTP_400_BAD_REQUEST)


class MessageInBoxListAPIView(views.APIView):
    '''自分に届いたメッセージリスト表示するAPI'''

    # authentication_classes = (TokenAuthentication,)
    # この設定があることで、jwtを持っていないと入れない
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
            yorozu_id = self.request.user.profile.yorozu_id
            # yorozu_idから自分に届いた、メッセージを取り出す
            queryset = Message.objects.filter(
                receiver_yorozu_id=yorozu_id).order_by('-created_at')
            serializer = MessageSerializer(instance=queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response("認証")
        except:
            return Response("認証なし", status=status.HTTP_401_UNAUTHORIZED)


# ==================================================================
# self.request.userに関して 2020 5 30
# tokenがある場合、self.request.userでユーザー情報を取り出すことができる
# self.request.user.profile.yorozu_idは、self.request.userで
# ユーザーを取り出し、そのあと、リレーションしているプロフィールモデルから、
# yorozu_idを取り出している
# ==================================================================

# ==================================================================
# Authに関して 2020 5 22
# permission_classes = (IsAuthenticated,)
# permission_classes に IsAuthenticated をすることでで認証済みでないと
# 実行できないAPIとなる。つまり、認証・登録ずみのユーザーのみアクセス許可
# ==================================================================


# ==================================================================
# request.dataで中身を見れる
# def create(self, request):
#     print(request.data)
#     return "aaa"
# ==================================================================


# class MyMessageBox(generics.ListAPIView):

#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer

#     def get_queryset(self):
#         return super().get_queryset()
