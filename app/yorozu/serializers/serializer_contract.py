from rest_framework import serializers
from ..models import Contract, Profile
from .serializer_plan import PlanSerializer


class GetContractSerializer(serializers.ModelSerializer):
    """契約に関してのシリアライザー(get)"""

    # 以下のようにすることで、ネストした値を受け取ることができる
    contract_plan = PlanSerializer(read_only=True)
    contract_yorozuya_name = serializers.SerializerMethodField()
    purchaser_user_name = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        # fields = '__all__'
        fields = ("sender_yorozu_id", "receiver_yorozu_id",
                  "contract_plan", "is_approval", "contract_yorozuya_name", 'purchaser_user_name', "created_at", "updated_at")

    def get_contract_yorozuya_name(self, instance):
        '''契約しているよろずやの名前'''
        # receiver_yorozu_idは、profileとリレーションしてあるので、以下のようなことができる
        # return instance.receiver_yorozu_id.nickname
        return instance.receiver_yorozu_id.yorozuya_name

        # ================================================================================
        # 2020 6 20
        # instanceには、今回であれば、それぞれのプランが入っている。
        # つまり、fieldで定義したカラムをもつオブジェクトが入っているので、
        # 「instance.receiver_yorozu_id」や「instance.is_approval]で、値を参照することができる。
        # ================================================================================

    def get_purchaser_user_name(self, instance):
        '''プランを購入してくれた人のよろずやの名前'''
        return instance.sender_yorozu_id.nickname


class PostContractSerializer(serializers.ModelSerializer):
    """契約に関して登録する時のシリアライザー(post)"""

    # 以下のようにすることで、ネストした値を受け取ることができる
    # contract_plan = PlanSerializer(read_only=True)

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
