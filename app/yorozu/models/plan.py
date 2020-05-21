import uuid
from django.db import models
from datetime import datetime


class Tag(models.Model):
    """タグ"""

    class Meta:
        # 管理画面でアプリのタイトルの名前を変更
        verbose_name_plural = "タグ"

    name = models.CharField("名称", max_length=64, unique=True, blank=True)

    @classmethod
    def get_or_create(cls, tag):
        """指定された名称のタグを生成して返す、既にあればそれを取得して返す"""
        # データがなかった場合Noneを返す
        ret = cls.objects.filter(name=tag).first()
        if not ret:
            # オブジェクトの作成と保存を一つの処理で行う
            ret = cls.objects.create(name=tag)
        return ret

    # ============================================================
    # objects.create(name=name)
    # オブジェクトの作成と保存を一つの処理で行う

    # (1)と(2)は同じ
    # (1) p = Person.objects.create(first_name="Bruce", last_name="Springsteen")
    # (2) p = Person(first_name="Bruce", last_name="Springsteen")
    #     p.save(force_insert=True)
  # ============================================================

    @classmethod
    def multi_get_or_create(cls, validated_data):

        # ex)validated_data: {'title': '企画屋',..... 'price': 122, 'tags': '記念日,インスターグラマー'}
        validated_data_tags = validated_data.get("tag")

        # 記念日,インスターグラマー => ['インスターグラマー', '記念日']
        tag_list = validated_data_tags.split(",")

        # ['企画', 'インスタ']
        no_ordered_dict_tags = []

        tags = []
        if not tag_list:
            return []
        for tag in tag_list:
            # 入力されたタグからタグを作成する
            tags.append(Tag.get_or_create(tag))
        return tags

    def __str__(self):
        return self.name


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
    created_at = models.DateTimeField("作成日", default=datetime.now)
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
