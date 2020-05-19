from rest_framework import status, views
from ..models import Plan
from rest_framework.response import Response
from ..serializers.serializer_plan_post import PlanPostSerializer

# ===================================================================
# プラン作成に関して、タグがリストのため、views.APIViewを使う
# 画像と配列を一緒に送ると全ての値が文字列になるの、viewssetは使えない
# プランの一覧を見るときは、views_planを使う
# ===================================================================


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
