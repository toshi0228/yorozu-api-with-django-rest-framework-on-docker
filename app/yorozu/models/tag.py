import uuid
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    """タグ"""

    class Meta:
        # 管理画面でアプリのタイトルの名前を変更
        verbose_name_plural = "タグ"

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField("名称", max_length=64, unique=True, blank=True)
    created_at = models.DateTimeField("作成日", default=timezone.now)
    updated_at = models.DateField("更新日", auto_now=True)

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
