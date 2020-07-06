from rest_framework import serializers
from ..models import Message, Profile
from .serializer_profile import ProfileSerializer


class MessageSerializer(serializers.ModelSerializer):

    sender_profile = serializers.SerializerMethodField()

    class Meta:
        model = Message

        fields = ("id", "sender_yorozu_id", "receiver_yorozu_id",
                  "message_content", "sender_profile", "unread", "created_at", "updated_at")

    def get_sender_profile(self, instance):
        '''送信者のプロフィールを取り出す'''

        # 引数instanceで受け取ったMessageインスタンスをprofileモデルの関数に渡す。
        sender_profile = Profile.get_prfofile_image(instance)

        # 送信者のプロフィールオブジェクトをシリアライザーに渡す
        serializers = ProfileSerializer(instance=sender_profile)

        sender_profile = {
            "nickname": serializers.data["nickname"],
            "yorozuya_name": serializers.data["yorozuya_name"],
            "profile_image": serializers.data["profile_image"],
        }
        return sender_profile


# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# シリアライザーのcreateのオーバーライドではviewsでモデルの型チェックを行ったデータが入ってくる
# is_valied()を呼び出さないとcreateも,実装されない
# viewssetに以下のようなコードをかいても意味がない

# def create(self, validated_data):
#     print("messageシリアライザ")
#     print(validated_data)
#     return
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
