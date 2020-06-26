from django.conf import settings
from django.db import models
from .plan import Tag
from django.utils import timezone


# # よろず屋プロフィール

class Profile(models.Model):
    class Meta:
        # 管理画面でアプリのタイトルの名前を変更
        verbose_name_plural = "プロフィール"
        # app_label = 'yorozu'

    # primary_key=Trueにすることで、主キーになる
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="アカウント情報")

    # primary_key=Trueにすることで、主キーになる
    # よろずIDはprofileのIDでもあり、profile詳細ページのURLになる
    yorozu_id = models.CharField(
        "YOROZU ID", max_length=20, default="", primary_key=True)
    nickname = models.CharField("ニックネーム", max_length=10)
    yorozuya_name = models.CharField("万屋の名前", max_length=10, default="")
    profile_image = models.ImageField("プロフィール画像", upload_to='', default="")
    plan_thumbnail_image = models.ImageField("サムネ画像", upload_to='', default="")
    profile_description = models.TextField("プロフィール説明", max_length=255)

    # review_score = models.IntegerField("レビュースコア")

    # twitter_account = models.CharField(
    #     "twitterのアカウント", max_length=80, default="", blank=True)

    # instagram_account = models.CharField(
    #     "instagramのアカウント", max_length=80, default="", blank=True)

    # facebook_account = models.CharField(
    #     "facebookのアカウント", max_length=80, default="", blank=True)

    created_at = models.DateTimeField("作成日", default=timezone.now)
    updated_at = models.DateField("更新日", auto_now=True)

    @classmethod
    def get_prfofile_image(cls, MessageInstance):
        # 送信者のyorozu_idから,送信者のプロフィールを持ってくる
        sender_profile = cls.objects.filter(
            yorozu_id=MessageInstance.sender_yorozu_id.yorozu_id).first()
        # 送信者のプロフィールから、プロフィール画像を取り出す
        return sender_profile

    def __str__(self):
        # タイトルの名前を押して詳細に入ったときの名前を変更できる
        # return self.yorozuya_name
        return self.yorozuya_name


# ===================================================================
# MessageInstance.sender_yorozu_id.yorozu_idに関して

# serializer_messageからMessageInstanceが届く。
# MessageInstanceから、sendernのよろずIDを取り出すために、
# MessageInstance.sender_yorozu_idをかく。
# そして、このsender_yorozu_idのフィールドは、Profileモデルを参照している
# ために、さらにMessageInstance.sender_yorozu_id.yorozu_idを取り出す
# ===================================================================
