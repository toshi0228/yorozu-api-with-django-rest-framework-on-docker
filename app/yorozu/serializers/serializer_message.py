from rest_framework import serializers
from ..models import Message


class MessageSerializer(serializers.ModelSerializer):

    message_list = serializers.SerializerMethodField()

    class Meta:
        model = Message

        fields = ("sender_yorozu_id", "receiver_yorozu_id",
                  "message_content", "message_list", "created_at", "updated_at")

    def get_message_list(self, instance):
        # print(instance)
        return "a"

        # receiver_yorozu_id

        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
        # シリアライザーのcreateのオーバーライドではviewsでモデルの型チェックを行ったデータが入ってくる
        # is_valied()を呼び出さないとcreateも,実装されない
        # viewssetに以下のようなコードをかいても意味がない

        # def create(self, validated_data):
        #     print("messageシリアライザ")
        #     print(validated_data)
        #     return
        # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
