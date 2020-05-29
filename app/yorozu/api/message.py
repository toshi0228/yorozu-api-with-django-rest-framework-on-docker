from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
# from rest_framework import generics
from ..models import Message
from ..serializers.serializer_message import MessageSerializer


class MessageListCreateAPIView(views.APIView):
    '''メッセージの一覧と作成APIクラス'''

    def get(self, request):
        # querysetはリスト(iterable)なので、引数にmany=Trueが必要
        queryset = Message.objects.all()
        serializer = MessageSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("登録完了")
        print("登録失敗")
        return Response("登録失敗", status=status.HTTP_400_BAD_REQUEST)


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
            queryset = Message.objects.filter(receiver_yorozu_id=yorozu_id)
            serializer = MessageSerializer(instance=queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response("認証")
        except:
            return Response("認証なし", status=status.HTTP_401_UNAUTHORIZED)


# ==================================================================
# self.request.userに関して　2020 5 30
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
