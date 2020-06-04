from django.test import TestCase
from django.contrib.auth import get_user_model

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
        self.assertEqual(user.email,email.lower())


    def test_new_user_invalid_email(self):
        '''メールアドレスがない場合に、エラーが起きるかどうかテスト'''

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None,password="test123")
            print(get_user_model().objects.create_user(email=None,password="test123"))

    
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
        print(user.is_superuser)
        self.assertTrue(user.is_staff)
        print(user.is_staff)




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
