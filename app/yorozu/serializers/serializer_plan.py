from rest_framework import serializers
from ..models import Plan, Tag
from .serializer_tag import TagSerializer


class PlanSerializer(serializers.ModelSerializer):

    # 以下のようにすることで、ネストした値を受け取ることができる
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = ('id', 'title', 'description', 'image',
                  'price', "tags", )

        # fields = ('title', 'tags',)
        # extra_kwargs = {
        #     # モデル上は必須フィールドだけれど、シリアライザでは Not必須にしたい場合は、required を上書きする
        #     'tags': {'required': False}
        # }


class PlanPostSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=15)
    description = serializers.CharField(max_length=255)
    image = serializers.ImageField(default="")
    price = serializers.IntegerField(default=0)
    tag = serializers.CharField(max_length=255)
    yorozuya_profile_id = serializers.CharField(max_length=255)

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # リレーション参照のフィールド名_idに関して 2020 6 22
    # リレーションしたモデルオブジェクトの主キーを扱うためには、planでつけた「フィールド名_id」なので
    # yorozuya_profile_idで、リレーション先の主キーを指定できる
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

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

# ===================================================================
# 2020 4 29
# djangoは、自動でモデルが追加される。idがプライマリーキー(pk)になる
# ===================================================================


# ===================================================================
# プラン作成に関して、modelserializerを使いたいが、modelserializerを使うと
# tagに関して、型チェックでエラーが起きてしますのでdefaultのserializerを使う
# ===================================================================
