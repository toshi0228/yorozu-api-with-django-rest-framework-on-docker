from rest_framework import serializers
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ("sender_yorozu_id", "receiver_yorozu_id",
                  "is_positive_score", "is_negative_score", "created_at")
