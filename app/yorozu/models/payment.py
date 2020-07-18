import uuid
from django.db import models
from django.utils import timezone


class Payment(models.Model):
    '''支払い内容に関して（モデルで管理しない決済情報に関して）'''

    class Meta:
        verbose_name_plural = '支払い'

    # id =注文ナンバー
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    price = models.PositiveIntegerField("料金", default=0)

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
