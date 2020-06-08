import uuid
from django.db import models
from django.utils import timezone
from .tag import Tag


class Plan(models.Model):
    class Meta:
        # 管理画面でアプリのタイトルの名前を変更
        verbose_name_plural = "プラン"

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField("プランタイトル", max_length=255)
    description = models.TextField("プランの説明", max_length=255)
    image = models.ImageField("イメージ画像", upload_to='', default="")
    price = models.PositiveIntegerField("料金", default=0)
    tags = models.ManyToManyField(Tag, blank=True)

    # 参照先を外部のモデルに持つ時、ForeignKeyは循環参照が起きないように、第一引数を文字列にできる
    yorozuya_profile = models.ForeignKey(
        "Profile", null=True,  on_delete=models.CASCADE, default="", verbose_name="作成者")
    created_at = models.DateTimeField("作成日", default=timezone.now)
    updated_at = models.DateField("更新日", auto_now=True)

    # プランのデータをfilterして取得できる
    # idによってplanデータをリストで取得してくる
    @classmethod
    def multi_get_filter_plan(cls, profileInstance):
        return cls.objects.filter(yorozuya_profile=profileInstance)

    def __str__(self):
        # タイトルの名前を押して詳細に入ったときの名前を変更できる
        return self.title

# =====================================================================================

# ImageField.upload_toはアップロード先のパスで、
# settings.pyで設定したMEDIA_ROOT以下のパスを指定します。
# 上記の例だとMEDIA_ROOT/images/に保存される

# =====================================================================================
