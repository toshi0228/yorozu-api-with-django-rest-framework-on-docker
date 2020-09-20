from django.shortcuts import get_object_or_404
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
    """決済の処理をしたユーザーの登録、編集"""

    # これがあるだけで、JWTがなければエラーになる
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """stripeから発行された顧客情報を取得する"""
        stripe.api_key = os.environ.get('STRIPE_KEY')

        # request.data["id"]より、request.data.get("id")の方が良い request.data["id"]だとidが渡って来ない時にエラーになる
        # request.data.get("id")であれば、もしIDがない場合にNoneを返す

        try:
            # tokenがある場合、self.request.userでユーザー情報を取り出すことができる
            app_id = self.request.user.profile.yorozu_id

            # app_idに紐づいている、strpeから発行されたtokenを取り出す
            queryset = Payment.objects.filter(app_id=app_id).first()

            # もしまだ,PaymentMethodIdなど登録したことがなければ空白を返す
            if queryset is None:
                return Response("")

            # querysetはリスト(iterable)の場合は、引数にmany=Trueが必要
            serializer = PaymentSerializer(instance=queryset)

            # stripeの処理 カード情報から顧客情報を取得する
            customer = stripe.PaymentMethod.retrieve(
                serializer.data["payment_method_id"]
            )

            return Response(customer, status=status.HTTP_200_OK)
        except:
            return Response("error", status=HTTP_500_INTERNAL_SERVER_ERROR)

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

            # returnととしては、カード情報と顧客情報を紐づいたもの取得するために、retrieveを使う
            customer = stripe.PaymentMethod.retrieve(
                serializer.data["payment_method_id"]
            )

            return Response(customer, status=status.HTTP_201_CREATED)
        else:
            return Response("エラー")

        # stripe.Customer.createで,metadataでuserIdを送ることで、stripe側で重複判定の処理を行うことができ、重複を防ぐことができる
        # metadata={"user_id": request.data['id']}

    def patch(self, request):
        """顧客情報の更新"""

        request.data["prev_payment_method_id"]

        stripe.api_key = os.environ.get('STRIPE_KEY')

        # カード情報と顧客情報と切り離す
        customer = stripe.PaymentMethod.detach(
            request.data["prev_payment_method_id"],
        )

        # 新しいカード情報と顧客情報を紐づける
        customer = stripe.PaymentMethod.attach(
            request.data["next_payment_method_id"],
            customer=request.data["customer_id"],
        )

        # 以下からは、サーバーサイドで、stripeから発行された顧客情報とカード情報のトークンを更新する処理
        app_id = self.request.user.profile.yorozu_id
        stripe_info = {
            "customer_id": customer["customer"],
            'payment_method_id': customer['id'],
            "app_id": app_id,
        }

        # payment_method_idが同じオブジェクトを取得(過去のものを更新するために古いprev_payment_method_idを使う)
        payment = get_object_or_404(
            Payment, payment_method_id=request.data["prev_payment_method_id"])

        # シリアライザーの初期値と、更新したいデータ、partial=Trueの3点セットで値が部分的に更新される
        serializer = PaymentSerializer(
            instance=payment, data=stripe_info, partial=True)

        if serializer.is_valid():
            serializer.save()

            # returnととしては、カード情報と顧客情報を紐づいたもの取得するために、retrieveを使う
            customer = stripe.PaymentMethod.retrieve(
                serializer.data["payment_method_id"]
            )

            return Response(customer, status=status.HTTP_200_OK)
        else:
            return Response("エラー")
