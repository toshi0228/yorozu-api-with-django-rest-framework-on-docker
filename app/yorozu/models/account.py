import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from .profile import Profile

# マネージャーは、モデルとクエリーの中間にあるもの 変換器と言うところか
# パスワードをハッシュ化してデータベースに保存する
# マネージャーは、データベースに保存する前の下ごしらえ

# UserManagerクラスは、ユーザ名、メールアドレス、
# パスワードに関するメソッドを提供するBaseUserManagerを継承します
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('ユーザー登録には、メールアドレスが必要です')

        # normalize_emailは、@から始まるemailの大文字、小文字を変換する
        # ex)"Test@Gmail.com" -> Test@gmail.com
        # マネジャメソッドが自分の属しているモデルクラスを取り出すために self.model にアクセスできる
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # djangoのclIコマンドを使うときの設定
    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        # id_adminは必要ないかもしれない 2020 6/4
        # user.is_admin = True
        user.save(using=self._db)
        return user

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# AbstractBaseUserを利用してカスタマイズユーザーを作成する場合、
# BaseUserManagerを継承したカスタムマネージャーを実装する必要がある
# ログイン時の認証においてusername以外を利用したい場合は、
# AbstractBaseUserを継承したモデルであるカスタムユーザーを作成する必要がある
# AbstractBaseUserは最低限な機能だけを持っている。AbstractUserが持っているフィールドの幾つかを
# 消したり、大きな変更が必要な場合は、AbstractBaseUserが良い
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# 継承できるもの 使い分け
# django.contrib.auth.models.AbstractUser ※追加のみを行う場合
# django.contrib.auth.models.AbstractBaseUser ※基本属性の修正をする場合
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

# !!!あとでAbstractBaseUserで、継承されているdata_joinedという登録日も入れたい

class Account(AbstractBaseUser):

    class Meta:
        # 管理画面でアプリのタイトルの名前を変更
        verbose_name_plural = "アカウント"

    # jwtを使う場合は、変数名をuuidにしたらエラーになる jwtを作るさいにidというカラムを内部で参考にしている
    # acuutnモデルに関しては、変数名を変えるとややこしくなるので、あまり変更しない方が良い
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    # username = models.CharField("氏名", max_length=30, unique=False, default="")
    last_name = models.CharField('苗字(姓)', max_length=30, blank=True)
    first_name = models.CharField('名前(名)', max_length=30, blank=True)
    email = models.EmailField(verbose_name='メールアドレス',
                              max_length=255, unique=True)
    password = models.CharField(
        verbose_name="パスワード", max_length=255, unique=True)

    # is_activeがfalseだと、管理画面に入れない(論理削除の時、使う)
    is_active = models.BooleanField(verbose_name="アカウントの状態", default=True)
    is_staff = models.BooleanField(
        verbose_name="管理画面サイトのログイン権限", default=False)

    created_at = models.DateTimeField("作成日", default=timezone.now)
    updated_at = models.DateField("更新日", auto_now=True)

    # name = models.CharField(max_length=255)
    # date_of_birth = models.DateField()
    # is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    # mailを利用したログイン認証にする
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin


# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# objects = AccountManager()に関して 2020 6 3
# 標準のBaseUserManagerを使う代わりに、
# AccountManagerを使うということをDjangoに知らせています。 これにより、今後「create_user」、
# 「create_superuser」のメソッドを呼ぶときにUserManagerクラスの「create_user」、
# 「create_superuser」のメソッドが呼ばれるようになります。
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# datetimeとtimezonの違い 2020 6 4
# Pythonのdatetimeオブジェクトには２種類のオブジェクトがあります。
# awareオブジェクト： タイムゾーンの情報を持っている
# naiveオブジェクト : タイムゾーンの情報を持っておらず、協定世界時刻（UTC）と現地時間を区別しない

# なぜ、djagnoの中で、datetimeを使うと,9時間遅れた時間になるので、datatimeを使う
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
