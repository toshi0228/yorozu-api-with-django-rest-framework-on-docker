import uuid
from django.db import models
from django.utils import timezone
from .profile import Profile
from .plan import Plan


class Contract(models.Model):
    '''契約に関してのモデル'''

    class Meta:
        verbose_name_plural = '契約(本契約)'

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    sender_yorozu_id = models.ForeignKey(
        "Profile", verbose_name="リクエスト送信者", on_delete=models.CASCADE, related_name="contract_sender")

    receiver_yorozu_id = models.ForeignKey(
        "Profile", verbose_name="リクエスト受信者", on_delete=models.CASCADE, related_name="contract_receiver")

    contract_plan = models.ForeignKey(
        'Plan', verbose_name='契約をしたプラン', on_delete=models.CASCADE, related_name='contract_plan', default='')

    # リクエスト受信者(よろず屋)が承認したかどうか
    is_approval = models.BooleanField(verbose_name='契約の承認状態', default=False)

    created_at = models.DateTimeField("作成日", default=timezone.now)

    updated_at = models.DateField("更新日", auto_now=True)

    def __str__(self):
        return f'送り主:{self.sender_yorozu_id} 受信者:{self.receiver_yorozu_id}'
