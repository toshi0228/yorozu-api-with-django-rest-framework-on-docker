from rest_framework import serializers
from ..models import Contract
from .serializer_plan import PlanSerializer


class GetContractSerializer(serializers.ModelSerializer):
    """契約に関してのシリアライザー(get)"""

    # 以下のようにすることで、ネストした値を受け取ることができる
    contract_plan = PlanSerializer(read_only=True)

    class Meta:
        model = Contract
        # fields = '__all__'
        fields = ("sender_yorozu_id", "receiver_yorozu_id",
                  "contract_plan", "is_approval", "created_at", "updated_at")


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
