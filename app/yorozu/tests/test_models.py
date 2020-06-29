from django.test import TestCase
from django.contrib.auth import get_user_model

from yorozu import models
from ..models import Profile, Tag, Profile


def sample_user(email='sample@gmail.com', password='testpass'):
    """サンプルユーザーを作成する"""
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """ユーザー登録に関してのテスト"""

        email = "test@gmail.com"
        password = "Testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """emailの@から始まる部分の大文字を小文字に変換できているか"""
        # ex)"Test@Gmail.com" -> Test@gmail.com

        email = "test@Gmail.CoM"
        user = get_user_model().objects.create_user(email=email, password="test123")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''メールアドレスがない場合に、エラーが起きるかどうかテスト'''

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password="test123")

    def test_create_new_superuser(self):
        """スーパーユーザーを作った時のテスト"""

        user = get_user_model().objects.create_superuser(
            email="test@gmail.com",
            password="test123"
        )

        # is_superuser
        # この値が真なら、ユーザは明示的な指定がなくても全てのパーミッションをもつ
        # is_staff
        # この値が真なら、ユーザは管理画面サイトにアクセスできる

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """タグ作成され文字列で表示されるかテスト"""

        tag = models.Tag.objects.create(
            name="企画"
        )
        self.assertEqual(str(tag), tag.name)

    def test_plan_str(self):
        """プランが表示されるかテスト"""

        profile = Profile.objects.create(account_id=sample_user().id,
                                         yorozu_id="SampleYorozuId",
                                         nickname="テステス２",
                                         yorozuya_name="テスト屋",
                                         profile_image="",
                                         plan_thumbnail_image="",
                                         profile_description="サンプル説明")

        plan = models.Plan.objects.create(
            title="プランタイトル",
            description="サンプル説明",
            image="",
            price=12,
            yorozuya_profile=profile
        )

        self.assertEqual(str(plan), plan.title)

    def test_profile_str(self):
        """プロフィールが表示されるかテスト"""

        profile = Profile.objects.create(account_id=sample_user().id,
                                         yorozu_id="SampleYorozuId",
                                         nickname="テストニックネーム",
                                         yorozuya_name="テスト屋さん",
                                         profile_image="",
                                         plan_thumbnail_image="",
                                         profile_description="サンプル説明")

        self.assertEqual(str(profile), profile.yorozuya_name)

    def test_message_str(self):
        """メッセージモデルに関してのテスト"""

        # メッセージに関してのテストをするために、送信者と受信者の二人のユーザーを作成する

        # アカウント作成
        user1 = get_user_model().objects.create_user(
            email="sample1@gmail.com", password="password1")

        user2 = get_user_model().objects.create_user(
            email="sample2@gmail.com", password="password2")

        # プロフィール作成
        user1_profile = Profile.objects.create(account_id=user1.id,
                                               yorozu_id='sample1YorozuId',
                                               nickname='サンプル1',
                                               yorozuya_name='サンプル1屋',
                                               profile_image='',
                                               plan_thumbnail_image='',
                                               profile_description='サンプル1の説明')

        user2_profile = Profile.objects.create(account_id=user2.id,
                                               yorozu_id='sample2YorozuId',
                                               nickname='サンプル2',
                                               yorozuya_name='サンプル2屋',
                                               profile_image='',
                                               plan_thumbnail_image='',
                                               profile_description='サンプル2の説明')

        # user1がuser2にメッセージを送信
        message = models.Message.objects.create(
            sender_yorozu_id=user1_profile,
            receiver_yorozu_id=user2_profile,
            message_content='こんにちは user2, 私はuser1です',
            is_read=False
        )

        self.assertEqual(str(message), f'送り主:{message.sender_yorozu_id}')

        # ==================================================================
        # get_user_model()で,Userモデルへの参照をできるようになる
        # インスタンスのUserには、全てのユーザーデータが入っている
        # User.objects.all()で全てのデータの中身を見れる
        # ==================================================================
        # ==================================================================
        # check_password(password)に関して
        # 渡された文字列がこのユーザの正しい文字列ならば True を返します。
        # (このメソッドは比較時にパスワードのハッシュ処理を行います)
        # create_user()で作られた、パスワードがハッシュ値なのでそれが正しいか確かめる
        # ==================================================================
