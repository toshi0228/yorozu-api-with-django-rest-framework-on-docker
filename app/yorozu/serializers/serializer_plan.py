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
        # fields = ("id", 'title', 'description', 'image',
        #           'price', "tags", 'yorozuya_profile')

        # fields = ('title', 'tags',)
        # extra_kwargs = {
        #     # モデル上は必須フィールドだけれど、シリアライザでは Not必須にしたい場合は、required を上書きする
        #     'tags': {'required': False}
        # }

    # def get_sender_profile(self, instance):
    #     '''送信者のプロフィールを取り出す'''

    #     # 引数instanceで受け取ったMessageインスタンスをprofileモデルの関数に渡す。
    #     sender_profile = Profile.get_prfofile_image(instance)

    #     # 送信者のプロフィールオブジェクトをシリアライザーに渡す
    #     serializers = ProfileSerializer(instance=sender_profile)

    #     sender_profile = {
    #         "nickname": serializers.data["nickname"],
    #         "yorozuya_name": serializers.data["yorozuya_name"],
    #         "profile_image": serializers.data["profile_image"],
    #     }
    #     return sender_profile


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

# ===================================================================
# 2020 4 29
# djangoは、自動でモデルが追加される。idがプライマリーキー(pk)になる
# ===================================================================


# ===================================================================
# プラン作成に関して、modelserializerを使いたいが、modelserializerを使うと
# tagに関して、型チェックでエラーが起きてしますのでdefaultのserializerを使う
# ===================================================================
