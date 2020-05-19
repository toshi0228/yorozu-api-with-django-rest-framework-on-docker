from rest_framework import serializers
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ("id", "sender_yorozu_id", "receiver_yorozu_id",
                  "review_content", "review_score", "created_at")
