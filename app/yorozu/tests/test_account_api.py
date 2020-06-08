from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


# CREATE_USER_URL = /api/account/ に変換される
CREATE_USER_URL = reverse("yorozu:accountCreate")
TOKEN_URL = "/api/auth/jwt/create/"
# トークンを持っていれば、idとemailを取得できる
ME_URL = '/api/auth/users/me/'


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """accountAPIのテスト"""

    def setUp(self):
        self.Client = APIClient()

    # todo アカウント作成のテストは、JWTが必要になるので、あとで行う

    def test_create_valid_user_success(self):
        """ユーザーの作成のテスト"""

        payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass'
        }
        # emailとpasswordpostしたら、ユーザー登録できるか確認
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.all()

        # payloadで渡したパスワードが、ハッシュ化されているかチェック
        self.assertTrue(user[0].check_password(payload["password"]))

        # レスポンスデータにパスワードが入っていないかチェック
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """既にアカウントがある場合に、エラーできるかテスト"""

        payload = {'email': 'testuser@gmail.com', 'password': 'testpass'}
        # グローバルで定義した関数を使って、ユーザーを作成する
        create_user(**payload)

        # もう一度、同じemailとパスワードでユーザーを作成しようとする
        res = self.Client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """パスワードが5文字以下の場合、エラーが起きるかテスト"""
        payload = {'email': 'test@gmail.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # パスワードが短くて、エラーになったので、アカウントが登録されていないか確認
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        # エラーを期待する
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """データベースに登録されているユーザーしか、トークンを作成しないかテストする"""

        payload = {'email': 'testuser', 'password': 'testpass'}
        create_user(**payload)

        # データベースに登録した後に、トークンを取得しにいく
        res = self.Client.post(TOKEN_URL, payload)

        # res.dataの中身 => {'refresh': '●●●', 'access': '●●●'}
        self.assertIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """"間違ったパスワードを送った時は、エラーが起きるか確認"""

        create_user(email='test@gmail.com', password='testpass')
        payload = {'email': 'test@gmail.com', 'password': 'wrong'}

        res = self.Client.post(TOKEN_URL, payload)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_no_user(self):
        """データベースにユーザーを登録していない状態で、postした場合にエラーを起こすか確認"""

        payload = {'email': 'test@gmail.com', 'password': 'testpass'}
        res = self.Client.post(TOKEN_URL, payload)

        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_missgin_field(self):
        """パスワードを空白でトークンを作成しようとした場合にエラーになるか"""

        res = self.Client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unuthoized(self):
        """自分の情報を確認ページに行った時に、ヘッターにjwtがなければ、401になるか確認"""

        res = self.Client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):

    def setUp(self):
        self.user = create_user(
            email='test@gmail.com',
            password='testpass'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """jwtから、正しいユーザー情報を取得できるか確認"""

        res = self.client.get(ME_URL)
        # res.dataの中身 => {'id': '7e9b2d8a-4681-49a6-a0d1-38079ead442c', 'email': 'test@gmail.com'}
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # ログインした、ユーザーのemailがちゃんと戻ってくるかテスト
        self.assertEqual(res.data['email'], self.user.email)

    def test_post_me_not_allowed(self):
        """postメソッドが許可されていないことを確認"""

        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # =======================================================================
        # check_password(raw_password)に関して
        # rowデータのパスワードがユーザの正しいハッシュ化されたパスワードならば
        # True を返えす。
        # (このメソッドはテスト実行時にパスワードのハッシュ処理を行う)
        # =======================================================================

        # =======================================================================
        # assertNotEqualに関して
        # assertNotEqual(a, b)
        # a != bかを判断するもの
        # =======================================================================

        # =======================================================================
        # assertFalse(x)に関して
        # bool(x) is False つまり、うまくいかないことを予期する
        # =======================================================================

        # =======================================================================
        # **paramsに関して 2020 6 5
        # **をもつ値を引数にすると、abc=1, xyz='xyz'....みたいなkey,valueの値をいくらでも
        # 受け取ることができる。また、{'abc': 1, 'xyz': 'xyz'...}の値のkeyのみで
        # 受け取りたい時は、(*kwargs)みたいな形で、展開した値を取れる

        # def func(*args, **kwargs):
        #     print(args) => (1, 2, 3)
        #     print(*args) => 1 2 3
        #     print(kwargs) => {'abc': 1, 'xyz': 'xyz'}
        #     print(*kwargs) => abc xyz
        #     print(args, kwargs) => (1, 2, 3) {'abc': 1, 'xyz': 'xyz'}
        #     print({*args, *kwargs}) => {1, 2, 3, 'abc', 'xyz'}
        # func(1, 2, 3, abc=1, xyz='xyz')

        # ちなみにfunc(1, 2, 3, abc=1, xyz='xyz')の別の書き方
        # 関数呼び出し時に辞書オブジェクトに**をつけて引数に指定することで、
        # 展開してそれぞれの引数として渡すことも可能。

        # payload = {"abc":1, "xyz":'xyz'}
        # func(1, 2, 3, **payload) ==  func(1, 2, 3, abc=1, xyz='xyz')

        # =======================================================================
