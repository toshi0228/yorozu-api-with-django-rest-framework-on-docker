from rest_framework import views, status
from rest_framework.response import Response
# from rest_framework import generics
from ..models import Message
from ..serializers.serializer_message import MessageSerializer


# class ProfileListAPIView(views.APIView):

#     def get(self, request):
#         queryset = Profile.objects.all()
#         serializer = ProfileSerializer(instance=queryset, many=True)
#         return Response(serializer.data, status.HTTP_200_OK)

class MessageList(views.APIView):

    def get(self, request):
        queryset = Message.objects.all()
        # querysetはリスト(iterable)なので、引数にmany=Trueが必要
        serializer = MessageSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# !!ModelViewSetのviwsのVは大文字
# class MessageViewSet(viewsets.ModelViewSet):

#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer

# # ====================================
#     # request.dataで中身を見れる
#     # def create(self, request):
#     #     print(request.data)
#     #     return "aaa"
# # ====================================


# class MyMessageBox(generics.ListAPIView):

#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer

#     def get_queryset(self):
#         return super().get_queryset()
