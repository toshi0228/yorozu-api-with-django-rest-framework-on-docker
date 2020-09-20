import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from .profile import Profile
# contractとpyamentモデル違い
# contract => ダッシュボードページなどで、データを管理
# pyament =>  stripeを使ってカード情報を登録


class Payment(models.Model):
    '''支払い内容に関して（stripeを使って決済情報を管理）'''

    class Meta:
        verbose_name_plural = '支払い(Stripe)'

    # id =注文ナンバー
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    # profileを作成した時に作られるid (account_id)とは別のもの
    app_id = models.ForeignKey(
        "Profile", verbose_name="アプリID", on_delete=models.CASCADE, related_name="profile", null=True, default="")

    # strip側で、管理している顧客ID
    customer_id = models.CharField(
        verbose_name="customer_id(顧客ID)", max_length=255, default="")

    # stripe側でカード情報をtoken化したもの
    payment_method_id = models.CharField(
        verbose_name="payment_method_id(カード情報)", max_length=255, default="")

    created_at = models.DateTimeField("作成日", default=timezone.now)

    updated_at = models.DateField("更新日", auto_now=True)
