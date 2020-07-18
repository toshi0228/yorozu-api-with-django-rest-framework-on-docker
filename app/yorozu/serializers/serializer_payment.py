from rest_framework import serializers
from ..models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('id', 'price')


# from rest_framework import serializers
# from ..models import Message, Profile
# from .serializer_profile import ProfileSerializer


# class MessageSerializer(serializers.ModelSerializer):

#     sender_profile = serializers.SerializerMethodField()

#     class Meta:
#         model = Message

#         fields = ("id", "sender_yorozu_id", "receiver_yorozu_id",
#                   "message_content", "sender_profile", "unread", "created_at", "updated_at")
