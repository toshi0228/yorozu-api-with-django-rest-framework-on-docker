from rest_framework import status, views
from ..models import Plan
from rest_framework.response import Response
from ..serializers.serializer_plan import PlanSerializer, PlanPostSerializer

# ===================================================================
# プラン作成に関して、タグがリストのため、views.APIViewを使う
# 画像と配列を一緒に送ると全ての値が文字列になるの、viewssetは使えない
# プランの一覧を見るときは、views_planを使う
# ===================================================================

# class MessageListCreateAPIView(views.APIView):
#     '''メッセージの送信したメッセージ一覧とメッセージ作成APIクラス'''
#     # この設定があることで、jwtを持っていないと入れない
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         try:
#             # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
#             yorozu_id = self.request.user.profile.yorozu_id
#             # 送信者が自分のメッセージを取り出す
#             queryset = Message.objects.filter(sender_yorozu_id=yorozu_id)
#             # querysetはリスト(iterable)なので、引数にmany=Trueが必要
#             serializer = MessageSerializer(instance=queryset, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except:
#             return Response("認証なし", status=status.HTTP_401_UNAUTHORIZED)

#     def post(self, request):
#         serializer = MessageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         print("登録失敗")
#         return Response("登録失敗", status=status.HTTP_400_BAD_REQUEST)


# class MessageListCreateAPIView(views.APIView):

class PlanListCreateAPIView(views.APIView):
    """プランの一覧"""

    def get(self, request):
        queryset = Plan.objects.all()
        serializer = PlanSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#     def get(self, request):
#         try:
#             # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
#             yorozu_id = self.request.user.profile.yorozu_id
#             # 送信者が自分のメッセージを取り出す
#             queryset = Message.objects.filter(sender_yorozu_id=yorozu_id)
#             # querysetはリスト(iterable)なので、引数にmany=Trueが必要
#             serializer = MessageSerializer(instance=queryset, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)


class PlanView(views.APIView):
    serializer_class = PlanPostSerializer

    def get(self, request, *args, **kwargs):
        return Response({"message": "planリストはviews_planでリクエスト処理をする"})

    def post(self, request):
        # print(request.body.get("profileDescription"))
        # print(request.body)
        print(request.data)
        # -------------------------------------------------------------------------------
        # request.bodyは、axiosで送られてきた、データがバイト型になっている。
        # request.dataは、axiosで送られてきた、データが辞書型になっている。
        # -------------------------------------------------------------------------------
        serializer = self.serializer_class(data=request.data)

        # -------------------------------------------------------------------------------
        # is_valid()で、PlanPostSerializerで定義したフィールドのバリデーションを行なっている
        # -------------------------------------------------------------------------------
        if serializer.is_valid():

            # ----------------------------------------------------------------------
            # serializer.save()を行うと、seriarizerのcreateメソッドが動く
            # is_valid()を行なったあとでないと、save()はできない
            # ----------------------------------------------------------------------
            serializer.save()

            # ----------------------------------------------------------------------
            # serializer.dataで、インスタンスを辞書型で取り出せるが、PlanPostSerializerで
            # 定義したタグがモデルではarrayだが、stringで定義しているのでうまくできない
            # ----------------------------------------------------------------------
            # serializer.data

            return Response("プラン登録成功")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
