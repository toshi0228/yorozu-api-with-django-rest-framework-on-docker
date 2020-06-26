from django.urls import path, include
from yorozu.api import profile, account, message, review, tag, contract, plan


# ======================================================================
# router
# router.register('register', views.AccountViewSet)
# router.register()の引数がurlになる エンドポイントになる
# ex)
# http://127.0.0.1:8081/account/register/
# ======================================================================


app_name = 'yorozu'

urlpatterns = [
    path('account/', account.AccountCreateAPIView.as_view(), name='accountCreate'),
    path('account/<pk>/', account.AccountRetrieveAPIView.as_view()),
    path('profile/', profile.ProfileListCreateAPIView.as_view()),
    path('profile/<pk>/', profile.ProfileRetrieveAPIView.as_view()),
    # path('profile/search/', profile.SearchProfileAPIView.as_view()),
    path('search/profile/', profile.SearchProfileAPIView.as_view()),
    path('plan/', plan.PlanListCreateAPIView.as_view(), name='plan'),
    path('message/', message.MessageListCreateAPIView.as_view()),
    path('messagebox/', message.MessageInBoxListAPIView.as_view()),
    path('review/', review.ReviewListAPIView.as_view()),
    path('tag/', tag.TagListAPIView.as_view(), name='tag-list'),
    path('contract/', contract.ReceiveContractListCreateAPIView.as_view()),
    path('contract/me/', contract.MySentContractListAPIView.as_view()),
]


# ===============================================================================
# app_nameに関して
# app_name = includeされたアプリ側の urls.py で指定するプロジェクトにおける名前空間
# app_name = 'yorozu'と書いておけば、testでurlを呼び出すときに、
# reverse('yorozu:accountCreate') のように参照できるようになる。
# 上記では yorozu/ 配下のURLは "yorozu" という名前空間になります。
# ===============================================================================
