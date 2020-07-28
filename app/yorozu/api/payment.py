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
        print("----------------------------------")
        print("ストライプに関して")
        print(request.data)
        print(request.data['id'])

        # これを先にstripeに渡さないとエラーになってしまう
        stripe.api_key = os.environ.get('STRIPE_KEY')

        # token = 'pk_test_51H2sQ2Ac2aWSlNWdWo97wMYthmjx2goPgJOXscnmHSOYRjGSBOgEpj6jn2JIIXhILpRvlDSgEOMUqk1Fs0f0fPoe00rUKABZcB'
        customer = stripe.Customer.create(email='etoshi0228@gmail.com')
        # print("customer表示ーーーーーーー")
        # print(customer.id)
        # email='etoshi0228@gmail.com', source=request.data['id'])

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
