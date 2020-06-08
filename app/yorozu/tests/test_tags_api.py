from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from ..models.plan import Tag

from ..serializers.serializer_tag import TagSerializer

TAGS_URL = reverse('yorozu:tag-list')


class PublicTagsApiTests(TestCase):
    """一般の人がタグAPIを利用できるかテスト"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tags(self):
        """タグリストを取得できるかテスト"""

        Tag.objects.create(name="インスタグラマー")
        Tag.objects.create(name="企画")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-id')
        serializer = TagSerializer(tags, many=True)
        # print()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
