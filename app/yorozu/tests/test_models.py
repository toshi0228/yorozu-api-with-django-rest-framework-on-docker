from django.test import TestCase
from django.contrib.auth import get_user_model

from yorozu import models
from ..models import Profile, Tag


def sample_user(email='test@gmail.com', password='testpass'):
    """サンプルユーザーを作成する"""
    return get_user_model().objects.create_user(email, password)


# プランのテストの時に必要
def sample_profile(nickname="テスト", yorozuya_name="テスト屋", profile_image="", plan_thumbnail_image="",
                   profile_description="テストテキスト", review_score=2, twitter_account="",  instagram_account="", facebook_account=""):
    """サンプルユーザーを作成する"""

    return Profile.objects.create(account_id=sample_user().id, nickname=nickname, yorozuya_name=yorozuya_name, review_score=1)


# プランのテストの時に必要
def sample_tag(name="サンプルのタグ"):
    """サンプルのタグを作成"""
    return Tag.objects.create(name=name)


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
            print(get_user_model().objects.create_user(
                email=None, password="test123"))

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
        """プランが表示されるか"""
        plan = models.Plan.objects.create(
            title="プランタイトル",
            description="サンプル説明",
            image="",
            price=12,
            yorozuya_profile=sample_profile(),
        )

        self.assertEqual(str(plan), plan.title)


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
