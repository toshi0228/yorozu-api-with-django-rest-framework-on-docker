from rest_framework import serializers
from ..models import Contract
from .serializer_plan import PlanSerializer


class ContractSerializer(serializers.ModelSerializer):
    """契約に関してのシリアライザー"""

    # 以下のようにすることで、ネストした値を受け取ることができる
    contract_plan = PlanSerializer(read_only=True)

    class Meta:
        model = Contract
        # fields = '__all__'
        fields = ("sender_yorozu_id", "receiver_yorozu_id",
                  "contract_plan", "is_approval", "created_at", "updated_at")
