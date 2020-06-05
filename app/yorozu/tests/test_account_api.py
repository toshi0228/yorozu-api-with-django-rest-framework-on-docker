from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("account:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """accountAPIのテスト"""

    def setUp(self):
        self.Client = APIClient()


    def test_create_valid_user_success():
        """ユーザーの作成のテスト"""

        payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        print(res)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().ojects.get(res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.asserNotIn('password',res.data)


    def test_user_exists(self):
        """既にアカウントがある場合に、エラーできるかテスト"""

        payload = {'email': 'testuser@gmail.com', 'password': 'testpass'}
        create_user(**payload)

        res = self.Client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.tatus_code, status.HTTP_400_BAD_REQUEST)

    
    def test_password_too_short(self):
        """パスワードが5文字以下の場合、エラーが起きるかテスト"""
        payload = {'email':'test@gmail.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


# =======================================================================
# check_password(raw_password)に関して
# 渡された文字列がこのユーザの正しい文字列ならば True を返します。 
# (このメソッドは比較時にパスワードのハッシュ処理を行います)
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

