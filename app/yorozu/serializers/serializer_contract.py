from rest_framework import serializers
from ..models import Contract, Profile
from .serializer_plan import PlanSerializer
from .serializer_profile import ProfileSerializer


class GetContractSerializer(serializers.ModelSerializer):
    """契約に関してのシリアライザー(get)"""

    # 以下のようにすることで、ネストした値を受け取ることができる
    contract_plan = PlanSerializer(read_only=True)

    contract_yorozuya_profile = serializers.SerializerMethodField()

    # # 自分のプランを購入してくれた人のプロフィール
    purchaser_profile = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        # fields = '__all__'
        fields = ("sender_yorozu_id", "receiver_yorozu_id",
                  "contract_plan", "is_approval", "contract_yorozuya_profile", 'purchaser_profile', "created_at", "updated_at")

    def get_contract_yorozuya_profile(self, instance):
        '''自分が契約しているよろずやのプロフィール'''

        # instance.receiver_yorozu_idで、送信者のprofileインスタンスを渡すことで、それに紐づいた情報が返ってくる
        # messageインスタンスに、profileがリレーションしているので、
        # instance.receiver_yorozu_idで、送信者のプロフィールインスタンスが返ってくる

        # 自分が契約しているよろずやのprofileを取得する
        contract_yorozuya_profile = Profile.get_prfofile_image(
            instance.receiver_yorozu_id)

        # # 契約しているよろずやのプロフィールオブジェクトをシリアライザーに渡す
        serializers = ProfileSerializer(instance=contract_yorozuya_profile)

        contract_yorozuya_profile = {
            "nickname": serializers.data["nickname"],
            "profile_image": serializers.data["profile_image"],
        }

        return contract_yorozuya_profile

        # ================================================================================
        # 2020 6 20 豆知識
        # instanceには、今回であれば、それぞれのプランが入っている。
        # つまり、fieldで定義したカラムをもつオブジェクトが入っているので、
        # 「instance.receiver_yorozu_id」や「instance.is_approval]で、値を参照することができる。

        # receiver_yorozu_idは、profileとリレーションしてあるので、以下のようなことができる
        # return instance.receiver_yorozu_id.nickname
        # ただ画像があると、ネストされたものから画像は取得できないので、モデルから取得する
        # ================================================================================

    def get_purchaser_profile(self, instance):
        '''プランを購入してくれた人のプロフィール'''

        # 引数instanceで受け取ったMessageインスタンスをprofileモデルの関数に渡す。
        sender_profile = Profile.get_prfofile_image(instance.sender_yorozu_id)

        # # 送信者のプロフィールオブジェクトをシリアライザーに渡す
        serializers = ProfileSerializer(instance=sender_profile)

        sender_profile = {
            "nickname": serializers.data["nickname"],
            "profile_image": serializers.data["profile_image"],
        }

        return sender_profile


class PostContractSerializer(serializers.ModelSerializer):
    """契約に関して登録する時のシリアライザー(post)"""

    class Meta:
        model = Contract
        # fields = '__all__'
        fields = ("sender_yorozu_id", "receiver_yorozu_id",
                  "contract_plan", "is_approval", "created_at", "updated_at")


# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# getとpostでシリアライザーを分ける理由

# シリアライザーに関してgetとpostで分けるのは、プランを登録した時に、idでとのプランとリレーションするかを
# 決めるのでIdでプランを特定して登録する

# getに関しては、どんなプランを登録したのか確認できるように、PlanSerializerをネストさせる
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
