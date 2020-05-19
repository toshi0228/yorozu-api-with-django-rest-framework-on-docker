from rest_framework import serializers
from ..models import Profile
from .serializer_plan import PlanSerializer
from ..models import Plan
from django.contrib.auth import get_user_model
# from django.conf import settings


class ProfileSerializer(serializers.ModelSerializer):
    # plan_list = PlanSerializer(many=True)
    # SerializerMethodFieldを使うことで、モデルに登録していないフィールドを自分で作ることができる。
    # SerializerMethodField は get_xxxx ってなっているメソッドをコールする
    plan_list = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "yorozu_id",
            "nickname",
            "profile_image",
            "profile_description",
            "yorozuya_name",
            "profile_image",
            "profile_description",
            "yorozu_main_image",
            "review_score",
            "twitter_account",
            "instagram_account",
            "facebook_account",
            "plan_list",

        )

    # "account_id"をfiledsに入れれば、account情報を呼び出せる

    # 引数instanceには、Profileモデルの値が入っている
    def get_plan_list(self, instance):
        # print(f'{"="*25}')
        # 以下でprofileのアカウント_idを取得できる
        # print(instance.account_id)

        # print(get_user_model())
        # print(settings.AUTH_USER_MODEL)
        # User = get_user_model()
        # print(User.objects.get(email="etoshi0228@gmail.com"))
        # user = User.objects.get(email="etoshi0228@gmail.com")
        # print(user.profile.yorozu_id)

        # プランモデルから、idに適合するモデルを引っ張ってくる
        filter_plan_list = Plan.multi_get_filter_plan(instance)

        # シリアライザーオブジェクトにJSON文字列もしくは、モデルオブジェクトを
        # 入れるとよしなに変換してくれる。今回の場合は、モデルの数が複数ある場合も
        # あるので,引数にmany=Trueを渡すことができる
        serializers = PlanSerializer(filter_plan_list, many=True)

        # serializers.dataで良い感じにjsonの形にしてくれる
        # ただ、ネストするとimageに関しては、http://127.0.0.1:8000がなくなるので
        # フロント側で自分で書かないといけない
        return serializers.data
