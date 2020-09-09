from rest_framework import serializers
from ..models import Message, Profile
from .serializer_profile import ProfileSerializer


class MessageSerializer(serializers.ModelSerializer):

    sender_profile = serializers.SerializerMethodField()
    receiver_profile = serializers.SerializerMethodField()

    class Meta:
        model = Message
        # fields = '__all__'
        fields = ("id", "sender_yorozu_id", "receiver_yorozu_id",
                  "message_content", "sender_profile", "receiver_profile", "unread", "created_at", "updated_at")

    def get_sender_profile(self, instance):
        '''送信者のプロフィールを取り出す'''

        # instance.sender_yorozu_idで、送信者のprofileインスタンスを渡すことで、それに紐づいた情報が返ってくる
        # messageインスタンスに、profileがリレーションしているので、
        # instance.sender_yorozu_idで、送信者のプロフィールインスタンスが返ってくる
        sender_profile = Profile.get_prfofile_image(instance.sender_yorozu_id)

        # 送信者のプロフィールオブジェクトをシリアライザーに渡す
        serializers = ProfileSerializer(instance=sender_profile)

        sender_profile = {
            "nickname": serializers.data["nickname"],
            "yorozuya_name": serializers.data["yorozuya_name"],
            "profile_image": serializers.data["profile_image"],
        }

        return sender_profile

    def get_receiver_profile(self, instance):
        '''受信者のプロフィールを取り出す'''

        receiver_profile = Profile.get_prfofile_image(
            instance.receiver_yorozu_id)

        # 送信者のプロフィールオブジェクトをシリアライザーに渡す
        serializers = ProfileSerializer(instance=receiver_profile)

        receiver_profile = {
            "nickname": serializers.data["nickname"],
            "yorozuya_name": serializers.data["yorozuya_name"],
            "profile_image": serializers.data["profile_image"],
        }

        return receiver_profile


# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# シリアライザーのcreateのオーバーライドではviewsでモデルの型チェックを行ったデータが入ってくる
# is_valied()を呼び出さないとcreateも,実装されない
# viewssetに以下のようなコードをかいても意味がない

# def create(self, validated_data):
#     print("messageシリアライザ")
#     print(validated_data)
#     return
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
