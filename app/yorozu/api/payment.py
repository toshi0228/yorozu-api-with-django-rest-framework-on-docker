import os
import stripe
from rest_framework import views, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from yorozu.models.payment import Payment
from yorozu.serializers.serializer_payment import PaymentSerializer


class PaymentAPIView(views.APIView):
    """stripe処理"""

    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response("ペイメント処理")

    def post(self, request):

        # これを先にstripeに渡さないとエラーになってしまう
        stripe.api_key = os.environ.get('STRIPE_KEY')

        # これでストライプ用の顧客情報を作成することができる
        # (あとでemailに関しては、編集 meta情報も追加した方が良いかもしれない)
        customer = stripe.Customer.create(email='etoshi0228@gmail.com')

        intent = stripe.PaymentIntent.create(
            customer=customer.id,
            amount=request.data['price'],
            currency='JPY',
            # payment_method_types=request.data['card'],
            # payment_method_types=['card'],
            # payment_method_types=request.data['id'],
            payment_method=request.data['id'],
            description=request.data['title'],
            receipt_email='etoshi0228@gmail.com',
            confirm=True,
        )

        return Response("ポスト処理成功")
