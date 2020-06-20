from ..models import Profile
from ..serializers.serializer_profile import ProfileSerializer, PostProfileSerializer
from rest_framework.response import Response
from rest_framework import status, views
from django.shortcuts import get_object_or_404


class ProfileListCreateAPIView(views.APIView):
    '''プロフィールのリストページ'''

    def get(self, request):
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(instance=queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):

        # PostProfileSerializerで型チェックを行う
        serializer = PostProfileSerializer(data=request.data)

        if serializer.is_valid():
            # sserializer.saveで,ProfileSerializerのclassでオーバライドさせておいたcreateメソッドが動く
            # ネストなど、していた複雑な値はここでカスタマイズする
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print("登録失敗")
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
        # serializer.is_valid()がfalseになる時 2020 6 20
        # serializer.is_valid()は、ただ型の確認をしているだけ、
        # 例えば,intergerなのに、strデータが入ってくるとエラーになる
        # また、必要なfieldが足りないかと行ってエラーになることはない。
        # 足りないフィールドがある場合は、serializer.save()でエラーになる
        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

        # return Response({})

    # def post(self, request):
    #     serializer = MessageSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_200_OK)
    #     print("登録失敗")
    #     return Response("登録失敗", status=status.HTTP_400_BAD_REQUEST)

    # jwtの場合、これは使わなくなるのかな..

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
