from rest_framework import serializers
from .serializer_tag import TagSerializer
from ..models import Plan, Tag

# ===================================================================
# プラン作成に関して、modelserializerを使いたいが、modelserializerを使うと
# tagに関して、型チェックでエラーが起きてしますのでdefaultのserializerを使う
# ===================================================================


class PlanPostSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=15)
    description = serializers.CharField(max_length=255)
    image = serializers.ImageField(default="")
    price = serializers.IntegerField(default=0)
    tag = serializers.CharField(max_length=255)
    profile_description = serializers.CharField(max_length=255)

    # 引数のvalidated_dataは、上記の型を確認したデータが入っている
    def create(self, validated_data):

        # タグの保存のクラスメソッド
        # ex)tag:[<Tag: 試し1>,<Tag: 試し2>]
        tag = Tag.multi_get_or_create(validated_data)

        # タグを削除して新たなオブジェクトを作成する
        # {'title': '企画屋',..... 'price': 122, 'tags': '記念日,インスターグラマー'}
        validated_data.pop('tag')

        # **validated_data {'title': '試し67'} => 'titile'='試し67'
        plan = Plan.objects.create(**validated_data)

        # セットの場合は配列にしないといけない
        plan.tags.set(tag)
        # print("この中身が知りたい")
        # print(plan.tags.all())

        return plan
