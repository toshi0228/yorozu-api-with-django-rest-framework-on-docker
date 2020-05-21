import uuid
from django.db import models
from datetime import datetime
from .profile import Profile


class Message(models.Model):
    '''メッセージモデル'''

    class Meta:
        verbose_name_plural = "メッセージ"

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    message_content = models.TextField("メッセージ内容", max_length=10)

    sender_yorozu_id = models.ForeignKey(
        "Profile", verbose_name="送信者", on_delete=models.CASCADE, related_name="sender", default="")

    receiver_yorozu_id = models.ForeignKey(
        "Profile", verbose_name="受信者", on_delete=models.CASCADE, related_name="receiver", default="")

    created_at = models.DateTimeField("作成日", default=datetime.now)
    updated_at = models.DateField("更新日", auto_now=True)

    def __str__(self):
        return f'送り主:{self.sender_yorozu_id}'

# dbshellでカラムの追加
# ALTER TABLE テーブル名 ADD COLUMN カラム名[ データ型];
