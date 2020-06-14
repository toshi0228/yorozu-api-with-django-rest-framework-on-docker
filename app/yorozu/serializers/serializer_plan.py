from rest_framework import serializers
from ..models import Plan, Tag
from .serializer_tag import TagSerializer


class PlanSerializer(serializers.ModelSerializer):

    # 以下のようにすることで、ネストした値を受け取ることができる
    tags = TagSerializer(many=True, read_only=True)
    # yorozuya_profile = ProfileSerializer()

    class Meta:
        model = Plan
        fields = ('id', 'title', 'description', 'image',
                  'price', "tags",)
        # fields = ("id", 'title', 'description', 'image',
        #           'price', "tags", 'yorozuya_profile')

        # fields = ('title', 'tags',)
        # extra_kwargs = {
        #     # モデル上は必須フィールドだけれど、シリアライザでは Not必須にしたい場合は、required を上書きする
        #     'tags': {'required': False}
        # }

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# 2020 4 29
# djangoは、自動でモデルが追加される。idがプライマリーキー(pk)になる
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
