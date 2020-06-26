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

        tag1 = Tag.objects.create(name="企画")
        tag2 = Tag.objects.create(name="インスタグラマー")

        res = self.client.get(TAGS_URL)

        # カラム名の前にハイフン（-）を書くと降順
        # ※メールソフトを開いて新しいメールが常に一番上に来ているなら、それは降順
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['name'], tag1.name)

    def test_create_tag_successful(self):
        """新しくタグを作るテスト"""

        payload = {'name': 'テストタグ'}
        self.client.post(TAGS_URL, payload)

        # .exists()は、存在すればTrueを返す
        exists = Tag.objects.filter(
            name=payload['name']
        ).exists()

        self.assertTrue(exists)
