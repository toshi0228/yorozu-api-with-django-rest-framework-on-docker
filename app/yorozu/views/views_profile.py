from rest_framework import viewsets, authentication
from ..serializers.serializer_profile import ProfileSerializer
from ..models import Profile
# from rest_framework.permissions import IsAuthenticated


class ProfileViewSet(viewsets.ModelViewSet):

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    # permission_classes = (IsAuthenticated,)

    # def retrieve(self, request, *args, **kwargs):
    #     print(f'{"="*25}')
    #     print(request.META)
    #     return super().retrieve(request, *args, **kwargs)

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# jwtを以下のコードでデコードできる
# import jwt
# jwt.decode(token, verify=False)
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝


# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# 認証に関して
# 以下の2つのコードを加える
# permission_classes = (IsAuthenticated,)
# from rest_framework.permissions import IsAuthenticated
# reactでheaderにtokenをつけてやると、表示、非表示ができる
# axios.defaults.headers.common['Authorization'] = `JWT ${auth}`;
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
