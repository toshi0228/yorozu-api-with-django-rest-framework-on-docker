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
        "YOROZU ID", max_length=32, default="", primary_key=True)
    nickname = models.CharField("ニックネーム", max_length=32)
    yorozuya_name = models.CharField("万屋の名前", max_length=32, default="")
    profile_image = models.ImageField("プロフィール画像", upload_to='', default="")

    yorozuya_thumbnail_image = models.ImageField(
        "よろず屋サムネ画像(トップページの画像)", upload_to='', default="")

    profile_description = models.TextField("プロフィール説明", max_length=255)

    created_at = models.DateTimeField("作成日", default=timezone.now)
    updated_at = models.DateField("更新日", auto_now=True)

    @classmethod
    def get_prfofile_image(cls, profile):
        # 送信者のyorozu_idから,送信者のプロフィールを持ってくる
        sender_profile = cls.objects.filter(
            yorozu_id=profile.yorozu_id).first()
        # 送信者のプロフィールから、プロフィール画像を取り出す
        return sender_profile

    @classmethod
    def get_contract_yorozuya_prfofile_image(cls, ContractInstance):
        # 送信者のyorozu_idから,送信者のプロフィールを持ってくる
        contract_yorozuya_profile = cls.objects.filter(
            yorozu_id=ContractInstance.receiver_yorozu_id.yorozu_id).first()
        # 送信者のプロフィールから、プロフィール画像を取り出す
        return contract_yorozuya_profile

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
