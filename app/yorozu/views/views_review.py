from rest_framework import viewsets
from ..models import Review
from ..serializers.serializer_review import ReviewSerializer


class MessageViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# # !!ModelViewSetのviwsのVは大文字
# class MessageViewSet(viewsets.ModelViewSet):

#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
