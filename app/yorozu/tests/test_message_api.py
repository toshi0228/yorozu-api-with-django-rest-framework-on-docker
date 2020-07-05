from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from yorozu.models.message import Message
from yorozu.models.profile import Profile

from yorozu.serializers.serializer_message import MessageSerializer


MESSAGE_URL = reverse('yorozu:sent-message-list')


class PublicMessageListCreateApiTests(TestCase):
    """JWTを持っていないユーザーは、取得に失敗するかテストする"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        "JWTに関してのテスト"

        res = self.client.get(MESSAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMessageListCreateApiTests(TestCase):
    """JWTに関してのテスト"""

    def setUp(self):
        self.client = APIClient()

        # メッセージに関してのテストをするために、送信者と受信者の二人のユーザーを作成する
        # アカウント作成
        self.user1 = get_user_model().objects.create_user(
            email="sample1@gmail.com", password="password1")

        self.user2 = get_user_model().objects.create_user(
            email="sample2@gmail.com", password="password2")

        # プロフィール作成
        self.user1_profile = Profile.objects.create(account_id=self.user1.id,
                                                    yorozu_id='sample1YorozuId',
                                                    nickname='サンプル1',
                                                    yorozuya_name='サンプル1屋',
                                                    profile_image='',
                                                    plan_thumbnail_image='',
                                                    profile_description='サンプル1の説明')

        self.user2_profile = Profile.objects.create(account_id=self.user2.id,
                                                    yorozu_id='sample2YorozuId',
                                                    nickname='サンプル2',
                                                    yorozuya_name='サンプル2屋',
                                                    profile_image='',
                                                    plan_thumbnail_image='',
                                                    profile_description='サンプル2の説明')

        self.client.force_authenticate(self.user1)

    def test_retrieve_message(self):
        """自分が送信したメッセージの一覧を取得できるかテスト"""

        message1 = Message.objects.create(
            sender_yorozu_id=self.user1_profile,
            receiver_yorozu_id=self.user2_profile,
            message_content='こんにちは user2, 私はuser1です(1回目)',
            is_read=False
        )

        message2 = Message.objects.create(
            sender_yorozu_id=self.user1_profile,
            receiver_yorozu_id=self.user2_profile,
            message_content='こんにちは user2, 私はuser1です(2回目)',
            is_read=False
        )

        res = self.client.get(MESSAGE_URL)

        # order_by('-created_at')をつける事で、一番最新のmessageを取得する
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_message_limited_to_user(self):
        """ユーザーごとにメッセージを取得できているかテスト"""

        # ユーザー1が送信したメッセージ
        user1_message = Message.objects.create(
            sender_yorozu_id=self.user1_profile,
            receiver_yorozu_id=self.user2_profile,
            message_content='こんにちは user2, 私はuser1です(1回目)',
            is_read=False
        )
        # ユーザー2が送信したメッセージ
        user2_message = Message.objects.create(
            sender_yorozu_id=self.user2_profile,
            receiver_yorozu_id=self.user1_profile,
            message_content='こんにちは user1, 私はuser2です(1回目)',
            is_read=False
        )

        # ユーザー1のJWT付きでアクセス
        res = self.client.get(MESSAGE_URL)

        # res = self.client.get(MESSAGE_URL)
        messages = Message.objects.filter(sender_yorozu_id=self.user1_profile)
        serializer = MessageSerializer(messages, many=True)

        # ユーザー1で取得した時は、ユーザー1が送信したデータのみ取得できているか
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_post_message(self):
        """メッセージ作成のテスト"""

        payload = {
            'sender_yorozu_id': self.user1_profile.yorozu_id,
            'receiver_yorozu_id': self.user2_profile.yorozu_id,
            'message_content ': 'こんにちは user2, 私はuser1です(2回目)',
            'is_read': False
        }

        res = self.client.post(MESSAGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        message = Message.objects.filter(id=res.data['id'])
        self.assertEqual(len(message), 1)

    # def test_patch_message(self):
    #     """メッセージの状態を未読から、既読にする"""
    #     todo

    # ==================================================================
    # テストで作られたデータに関して 2020 6 28
    # データはメソッドごとになくなっている
    # ==================================================================

    # ==================================================================
    # HTTPメソッドとmodelを作る時で、少し必要なデータ変わる 2020 6 28

    # メッセージモデルから,データを作る場合は、渡すデータはprofileオブジェクトを
    # そのまま渡せば良い

    # ex) モデルオブジェクト
    # user2_message = Message.objects.create(
    #     sender_yorozu_id=self.user2_profile,
    #     receiver_yorozu_id=self.user1_profile,
    #     message_content='こんにちは user1, 私はuser2です(1回目)',
    #     is_read=False
    # )

    # HTTPメソッドの場合は、しっかり値を渡さないといけない
    # self.user1_profile.yorozu_idをモデルに与えることで、モデルはどのprofileと
    # リレーションすればわかる

    # ex) HTTPメソッドの場合
    # payload = {
    #     'sender_yorozu_id': self.user1_profile.yorozu_id,
    #     'receiver_yorozu_id': self.user2_profile.yorozu_id,
    #     'message_content ': 'こんにちは user2, 私はuser1です(2回目)',
    #     'is_read': False
    # }

    # res = self.client.post(MESSAGE_URL, payload)
    # ==================================================================
