import os
import stripe
from rest_framework import views, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from yorozu.models.payment import Payment
from yorozu.serializers.serializer_payment import PaymentSerializer


class PaymentAPIView(views.APIView):
    """stripe決済処理"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response("ペイメント処理")

    def post(self, request):

        # これを先にstripeに渡さないとエラーになってしまう
        stripe.api_key = os.environ.get('STRIPE_KEY')

        # これでストライプ用の顧客情報を作成することができる
        # (あとでemailに関しては、編集 meta情報も追加した方が良いかもしれない emailはあとで変数を追加)
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


class CreatePaymentCustomer(views.APIView):
    """決済の処理をしたユーザーの登録"""

    # これがあるだけで、JWTがなければエラーになる
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        stripe.api_key = os.environ.get('STRIPE_KEY')
        print("---------------")
        # request.data["id"]より、request.data.get("id")の方が良い request.data["id"]だとidが渡って来ない時にエラーになる
        # request.data.get("id")であれば、もしIDがない場合にNoneを返す
        print(request.data.get("id"))

        a = stripe.Customer.retrieve(request.data.get("id"))
        print("---------------")
        print(a)

        return Response("stripe処理")

    def post(self, request):
        """顧客の作成"""

        # これを先にstripeに渡さないとエラーになってしまう
        stripe.api_key = os.environ.get('STRIPE_KEY')

        # request.data の中身例)
        # => {'id': 'e3f5c447-1a7f-4633-8874-17cf0348fc62', 'email': 'n@gmail.com', 'payment_method_id': 'pm_1HSK8nAc2aWSlNWdGQPd8RvW'}
        # idは、uuidで、accountと同じ情報になる

        # 顧客情報の登録
        customer = stripe.Customer.create(
            description='ユーザー', email=request.data['email'], payment_method=request.data['payment_method_id'], metadata={"user_id": request.data['id']})

        # request.userでログイン中のユーザーを取得することができる
        # ※今まで、peofileの主キーにyorozu_idを指定していたが、app_idと汎用的な名前に変更
        app_id = self.request.user.profile.yorozu_id

        # ストライプで必要な情報と、accountを紐づける
        stripe_info = {
            "customer_id": customer["id"],
            'payment_method_id': request.data['payment_method_id'],
            "app_id": app_id,
        }

        # stripeの決済情報に関してのシリアライザー
        serializer = PaymentSerializer(data=stripe_info)
        if serializer.is_valid():
            serializer.save()
            return Response(customer, status=status.HTTP_201_CREATED)
        else:
            return Response("エラー")

        # stripe.Customer.createで,metadataでuserIdを送ることで、stripe側で重複判定の処理を行うことができ、重複を防ぐことができる
        # metadata={"user_id": request.data['id']}
