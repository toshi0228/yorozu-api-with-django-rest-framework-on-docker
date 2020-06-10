from django.urls import path, include
from yorozu.api import profile, account, message, review, tag, request
from yorozu.views import (views_account,
                          views_plan,
                          views_tag,
                          api_view_plan,
                          views_profile,
                          views_message,
                          views_review
                          )
from rest_framework import routers


# ======================================================================
# router
# router.register('register', views.AccountViewSet)
# router.register()の引数がurlになる エンドポイントになる
# ex)
# http://127.0.0.1:8081/account/register/
# ======================================================================

router = routers.DefaultRouter()
router.register('accounts', views_account.AccountViewSet)
router.register('profiles', views_profile.ProfileViewSet)
router.register('plan', views_plan.PlanViewSet)
router.register('tags', views_tag.TagViewSet)
router.register('messages', views_message.MessageViewSet)
router.register('reviews', views_review.MessageViewSet)


app_name = 'yorozu'

urlpatterns = [
    path('', include(router.urls)),
    path('account/', account.AccountCreateAPIView.as_view(), name='accountCreate'),
    path('account/<pk>/', account.AccountRetrieveAPIView.as_view()),
    path('profile/', profile.ProfileListAPIView.as_view()),
    path('profile/<pk>/', profile.ProfileRetrieveAPIView.as_view()),
    path('message/', message.MessageListCreateAPIView.as_view()),
    path('messagebox/', message.MessageInBoxListAPIView.as_view()),
    path('review/', review.ReviewListAPIView.as_view()),
    path('tag/', tag.TagListAPIView.as_view(), name='tag-list'),
    path('request/', request.RequestListCreateAPIView.as_view()),
    path('request/me/', request.MyRequestListAPIView.as_view()),

    # path('accout', views_message.as_view())
]

# path('entry', views_plan_entry.api_entry),

# ===============================================================================
# app_nameに関して
# app_name = includeされたアプリ側の urls.py で指定するプロジェクトにおける名前空間
# app_name = 'yorozu'と書いておけば、testでurlを呼び出すときに、
# reverse('yorozu:accountCreate') のように参照できるようになる。
# 上記では yorozu/ 配下のURLは "yorozu" という名前空間になります。
# ===============================================================================
