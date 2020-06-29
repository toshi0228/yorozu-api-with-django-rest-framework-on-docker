import uuid
from django.db import models
from .profile import Profile
from django.utils import timezone


class Message(models.Model):
    '''メッセージモデル'''

    class Meta:
        verbose_name_plural = "メッセージ"

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    message_content = models.TextField("メッセージ内容", max_length=600)

    # profileの主キーはよろずIDなので、profileをリレーションしていということは、yorozu_idとリレーションしている
    sender_yorozu_id = models.ForeignKey(
        "Profile", verbose_name="送信者", on_delete=models.CASCADE, related_name="sender", default="")

    receiver_yorozu_id = models.ForeignKey(
        "Profile", verbose_name="受信者", on_delete=models.CASCADE, related_name="receiver", default="")

    is_read = models.BooleanField(verbose_name='既読判定', default=False,)

    created_at = models.DateTimeField("作成日", default=timezone.now)
    updated_at = models.DateField("更新日", auto_now=True)

    def __str__(self):
        return f'送り主:{self.sender_yorozu_id}'

# dbshellでカラムの追加
# ALTER TABLE テーブル名 ADD COLUMN カラム名[ データ型];
