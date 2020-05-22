from rest_framework import views, status
from rest_framework.response import Response
from ..models import Review
from ..serializers.serializer_review import ReviewSerializer


class ReviewListAPIView(views.APIView):

    def get(self, request):

        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # class MessageViewSet(viewsets.ModelViewSet):

        #     queryset = Review.objects.all()
        #     serializer_class = ReviewSerializer

        # # !!ModelViewSetのviwsのVは大文字
        # class MessageViewSet(viewsets.ModelViewSet):

        #     queryset = Message.objects.all()
        #     serializer_class = MessageSerializer
