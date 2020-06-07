from rest_framework import serializers
from ..models import Request


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ("sender_yorozu_id", "receiver_yorozu_id",
                  "isApproval", "created_at", "updated_at")
