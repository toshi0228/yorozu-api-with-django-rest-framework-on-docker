from django.shortcuts import get_object_or_404
from rest_framework import status, views
from ..models import Plan
from rest_framework.response import Response
from ..serializers.serializer_plan import PlanSerializer, PlanPostSerializer, PlanPatchSerializer

# ===================================================================
# プラン作成に関して、タグがリストのため、views.APIViewを使う
# 画像と配列を一緒に送ると全ての値が文字列になるの、viewssetは使えない
# プランの一覧を見るときは、views_planを使う
# ===================================================================


class PlanListCreateAPIView(views.APIView):
    """プランの一覧"""

    def get(self, request):
        queryset = Plan.objects.all()
        serializer = PlanSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        print(request.data)
        # -------------------------------------------------------------------------------
        # request.bodyは、axiosで送られてきた、データがバイト型になっている。
        # request.dataは、axiosで送られてきた、データが辞書型になっている。
        # -------------------------------------------------------------------------------
        # serializer = self.serializer_class(data=request.data)
        serializer = PlanPostSerializer(data=request.data)

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

            # 本当は、登録したプランをreturnしたいが、上手くいかないのでyrozuIdだけ渡す
            return Response(request.data['yorozuya_profile_id'], status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanUpdateAPIView(views.APIView):
    """プランの一部更新するAPI"""

    def patch(self, request, pk):

        # プランオブジェクトを取得
        plan = get_object_or_404(Plan, pk=pk)

        # シリアライザーの初期値と、更新したいデータ、partial=Trueの3点セットで値が部分的に更新される
        serializer = PlanPatchSerializer(
            instance=plan, data=request.data, partial=True)

        # serializer.save()を行うと、seriarizerのupdateメソッドが動く
        # is_valid()を行なったあとでないと、save()はできない
        if serializer.is_valid():
            serializer.save()

            # 本当は、登録したプランをreturnしたいが、上手くいかないのでplan_idだけ渡す
            return Response(pk, status=status.HTTP_200_OK)

        # serializer.is_valid()
        # print(serializer.data)
        return Response('NG', status=status.HTTP_400_BAD_REQUEST)
