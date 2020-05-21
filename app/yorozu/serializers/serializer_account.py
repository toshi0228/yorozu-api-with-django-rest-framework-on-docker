from rest_framework import serializers
from ..models import Plan
from ..models import Account
from .serializer_profile import ProfileSerializer
from django.contrib.auth import get_user_model


class AccountSerializer(serializers.ModelSerializer):

    yorozu_id = serializers.SerializerMethodField()

    class Meta:
        model = Account
        # fields = "__all__"
        fielfs = ('email', 'password' "yorozu_id")
        exclude = ("id", 'first_name', 'last_name', "username",
                   "is_active", "is_staff", "last_login")

        # 開発中はextra_kwargsをoffにしておく
        # extra_kwargs = {
        #     "email": {
        #         "write_only": True
        #     },
        #     "password": {
        #         "write_only": True
        #     }
        # }

        # =======================================================================
        #  extra_kwargsで"write_only": Trueにすることで書き込みだけしかできなくなる
        # =======================================================================

        # =======================================================================
        # 上書きでユーザーを作成する
        # シリアライザーでcreateを使うことでオーバーライドできる
        # 引数には、入力項目が入ってくる
        # =======================================================================

    def create(self, validated_data):
        user = Account.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    # 引数instanceには、Profileモデルの値が入っている

    def get_yorozu_id(self, instance):

        # ======================================================
        # get_user_model()で,Userモデルへの参照をできるようになる
        # インスタンスのUserには、全てのユーザーデータが入っている
        # User.objects.all()で全てのデータの中身を見れる
        # ======================================================
        User = get_user_model()

        # instance.idにはそれぞれのアカウントIDがあり、それを使い指定のuserを呼び出す
        user = User.objects.get(id=instance.id)

        # userとprfileは一対一リレーションを組んでいるので,yorozu_idを取り出せる
        # アカウントを作成したばかりの人は、profileがない場合もあるので,try,except
        try:
            yorozu_id = user.profile.yorozu_id
        except:
            yorozu_id = ""

        return yorozu_id

        # ======================================================
        # settings.AUTH_USER_MODELでも,ユーザーモデルを参照することが
        # できるが文字列になっている
        # ======================================================
