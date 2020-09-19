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
        "Profile", verbose_name="アプリID", on_delete=models.CASCADE, related_name="profile", default="")

    # strip側で、管理している顧客ID
    customer_id = models.CharField(
        verbose_name="customer_id(顧客ID)", max_length=255, default="")

    # stripe側でカード情報をtoken化したもの
    payment_method_id = models.CharField(
        verbose_name="payment_method_id(カード情報)", max_length=255, default="")

    created_at = models.DateTimeField("作成日", default=timezone.now)

    updated_at = models.DateField("更新日", auto_now=True)


# card: {id: "card_1H3I4DAc2aWSlNWdCaJGijMi", object: "card", address_city: null, address_country: null, address_line1: null, …}
# client_ip: "1.21.118.147"
# created: 1594371529
# email: "etoshi0228@gmail.com"
# id: "tok_1H3I4DAc2aWSlNWdPOnOgYJz"
# livemode: false
# object: "token"
# type: "card"
# used: false

# card:
# address_city: null
# address_country: null
# address_line1: null
# address_line1_check: null
# address_line2: null
# address_state: null
# address_zip: null
# address_zip_check: null
# brand: "Visa"
# country: "US"
# cvc_check: "unchecked"
# dynamic_last4: null
# exp_month: 2
# exp_year: 2022
# funding: "credit"
# id: "card_1H3I4DAc2aWSlNWdCaJGijMi"
# last4: "4242"
# metadata: {}
# name: "etoshi0228@gmail.com"
# object: "card"
# tokenization_method: null
