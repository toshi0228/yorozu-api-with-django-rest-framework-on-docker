from ..models import Profile
from ..models import Plan
from ..models import Tag
from ..serializers.serializer_profile import ProfileSerializer, PostProfileSerializer
from ..serializers.serializer_plan import PlanSerializer
from rest_framework.response import Response
from rest_framework import status, views
from django.shortcuts import get_object_or_404
from django.db.models import Q


class ProfileListCreateAPIView(views.APIView):
    '''プロフィール(よろず屋)のリストページ'''

    def get(self, request):
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(instance=queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        '''プロフィールの作成'''

        # PostProfileSerializerで型チェックを行う
        serializer = PostProfileSerializer(data=request.data)
        print(request.data)

        if serializer.is_valid():
            # sserializer.saveで,ProfileSerializerのclassでオーバライドさせておいたcreateメソッドが動く
            # ネストなど、していた複雑な値はここでカスタマイズする
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("登録失敗")
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # serializer.is_valid()がfalseになる時 2020 6 20
    # serializer.is_valid()は、ただ型の確認をしているだけ、
    # 例えば,intergerなのに、strデータが入ってくるとエラーになる
    # また、必要なfieldが足りないかと行ってエラーになることはない。
    # 足りないフィールドがある場合は、serializer.save()でエラーになる
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # authenticationは認証で、そのトークンがデータベースにあるかどうかを判断
    # permissionは、そのユーザーがログインしてあるユーザかどうか判断
    # プロフィルールなど、他の人に、編集やら削除されないために、pemisttiionをつける
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝


class ProfileRetrieveAPIView(views.APIView):
    '''プロフィールの詳細ページ'''

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(instance=profile)
        return Response(serializer.data, status.HTTP_200_OK)


class SearchProfileAPIView(views.APIView):
    '''プロフィール(よろず屋)の検索'''

    def post(self, request):

        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
        # タグでの検索
        # tag_queryset => <QuerySet [<Tag: 企画>, <Tag: 企画屋>]>
        tag_queryset = Tag.objects.filter(
            name__contains=request.data["keyword"])

        # tag_querysetがあった場合
        # [ < Plan: 似顔絵プラン > , < Plan: クルーン > ]
        plan_queryset = []

        # profileデータを取り出したが、まずはプランを取り出す
        # 逆参照の場合、オブジェクト.クラス名_setとすることで、クエリセットを取得できる
        for queryset in tag_queryset:
            plan_queryset.extend(queryset.plan_set.all())

        # plan_querysetがあった場合
        if plan_queryset:
            # planとリレーションしているprofileから、profileのquerysetを作りだす
            # [<Plan: サプライズプランだ>] => [<Profile: のびた屋>]
            profile_queryset = []

            for queryset in plan_queryset:
                profile_queryset.append(queryset.yorozuya_profile)

            # tagの場合、profileに重複があるので、同じものを統合する
            # [<Profile: しずかちゃん屋>,<Profile: しずかちゃん屋>] =>[<Profile: しずかちゃん屋>]
            _profile_queryset = list(set(profile_queryset))

            serializer = ProfileSerializer(
                instance=_profile_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

        # プランのタイトルで検索
        plan_queryset = Plan.objects.filter(
            title__contains=request.data["keyword"])

        # planとリレーションしているprofileから、profileのquerysetを作りだす
        # [<Plan: サプライズプランだ>] => [<Profile: のびた屋>]
        profile_queryset = []

        for queryset in plan_queryset:
            profile_queryset.append(queryset.yorozuya_profile)

        # プランでクエリセットが引っかかれば実行する
        if plan_queryset:
            serializer = ProfileSerializer(
                instance=profile_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
        # よろず屋の名前での検索、よろず屋オーナーのニックネームでの検索

        queryset = Profile.objects.filter(
            Q(yorozuya_name__contains=request.data["keyword"]) | Q(nickname__contains=request.data["keyword"]))

        if queryset:
            serializer = ProfileSerializer(
                instance=queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("検索条件にマッチしたものがありませんでした", status=status.HTTP_200_OK)

        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # jwtを以下のコードでデコードできる
    # import jwt
    # jwt.decode(token, verify=False)
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # 認証に関して
    # 以下の2つのコードを加える
    # permission_classes = (IsAuthenticated,)
    # from rest_framework.permissions import IsAuthenticated
    # reactでheaderにtokenをつけてやると、表示、非表示ができる
    # axios.defaults.headers.common['Authorization'] = `JWT ${auth}`;
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # querysetとは、Djangoが作っているQueryset型のデータ
    # querysetは、モデルから取り出した一連の情報
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # シリアライザーは、querysetや、オブジェクトをjsonデータに書き出す
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # serializer = ProfileSerializer(queryset, many=True)
    # many = Trueを引数で与えると、複数データの処理が可能に

    #  serializer = UserSerializer(data=[
    #     {'email': 'laugh_k@example.com','username': 'laugh_k', 'password': 'シークレットシークレット'},
    #     {'email': 'checkpoint@example.com','username': 'checkpoint', 'password': 'シークレットシークレット'}, ],
    # many=True)
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # シリアライザーに関して
    # serializer = ProfileSerializer(instance=queryset)
    # serializer.data
    # 引数のinstanceにモデルオブジェクトを指定して、シリアライザをインスタス化して,
    # JSON形式のデータに変換
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # シリアライザーに関して(バリデーションを行う場合）
    # 検証対象の入力データを引数を[data]に渡して、シリアライザをインスタンス化し,is_valid()を
    # 実行することで入力データをバリデーションを行うことができる
    # serializer = ProfileSerializer(data=queryset)
    # serializer.is_valid()
    # serializer._validated_data
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # __containsに関して 2020 6 25
    # name__contains = "みかん" であれば「有田みかん」「美味しいみかんジュース」などが返ります
    # ex) Product.objects.filter(name__contains="みかん", price__gte=100)
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
