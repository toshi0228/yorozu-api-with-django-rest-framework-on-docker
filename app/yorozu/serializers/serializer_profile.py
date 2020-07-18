from rest_framework import serializers
from ..models import Profile
from .serializer_plan import PlanSerializer
from ..models import Plan, Review
from django.contrib.auth import get_user_model
# from django.conf import settings


class ProfileSerializer(serializers.ModelSerializer):
    # plan_list = PlanSerializer(many=True)
    # SerializerMethodFieldを使うことで、モデルに登録していないフィールドを自分で作ることができる。
    # SerializerMethodField は get_xxxx ってなっているメソッドをコールする
    plan_list = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    # postive negative model

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
            # "plan_thumbnail_image",
            "yorozuya_thumbnail_image",
            "score",
            "plan_list",
        )

    # "account_id"をfiledsに入れれば、account情報を呼び出せる

    # 引数instanceには、Profileモデルの値が入っている
    def get_plan_list(self, instance):

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

    def get_score(self, instance):

        recieve_review_list = Review.objects.filter(
            receiver_yorozu_id=instance)
        # レビュがある場合は,true
        if recieve_review_list:
            positive_score = []
            negative_score = []

            for recieve_review in recieve_review_list:
                # trueの場合は、特点を追加する
                if recieve_review.is_positive_score:
                    positive_score.append(recieve_review.is_positive_score)

                if recieve_review.is_negative_score:
                    negative_score.append(recieve_review.is_negative_score)

            return {"positive_score": len(positive_score), "negative_score": len(negative_score)}

        return {"positive_score": 0, "negative_score": 0}


# ModelSerializerを使うと、ネストしていあるプランなど、余計なものがあるので、post用のシリアライザーを作成する
class PostProfileSerializer(serializers.Serializer):
    '''プロフィールを作成する時のシリアライザー'''

    account_id = serializers.CharField(max_length=255)
    yorozu_id = serializers.CharField(max_length=255)
    nickname = serializers.CharField(max_length=255)
    yorozuya_name = serializers.CharField(max_length=255)
    profile_image = serializers.ImageField(default="")
    # plan_thumbnail_image = serializers.ImageField(default="")
    yorozuya_thumbnail_image = serializers.ImageField(default="")
    profile_description = serializers.CharField(max_length=255)
    # review_score = serializers.IntegerField(default=0)
    # twitter_account = serializers.CharField(max_length=255, default="")
    # instagram_account = serializers.CharField(max_length=255, default="")
    # facebook_account = serializers.CharField(max_length=255, default="")

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)

        return profile
    # ==================================================================================
    # OneToOneFieldの逆参照に関して 2020 6 21
    # accountとprofiledでOneToOneFieldだがprofileからは、account_idと言う形でaccountの
    # 主キー(id)を参照することでできる
    # ==================================================================================

    # ==================================================================================
    # **validated_dataに関して 2020 6 21
    # 関数呼び出し時にオブジェクトに**をつけてしているすると要素にキーが引数名、値が引数の値として
    # 展開されて渡される
    # ex) obj = **{"id": 123} => id=123
    # ==================================================================================
