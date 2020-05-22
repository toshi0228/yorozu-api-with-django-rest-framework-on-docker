from django.urls import path, include
from yorozu.api import profile, account, message, review, tag
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

urlpatterns = [
    path('', include(router.urls)),
    path('account/', account.AccountCreate.as_view()),
    path('profile/', profile.ProfileListAPIView.as_view()),
    path('profile/<pk>/', profile.ProfileRetrieveAPIView.as_view()),
    path('message/', message.MessageList.as_view()),
    path('review/', review.ReviewListAPIView.as_view()),
    path('tag/', tag.TagListAPIView.as_view())

    # path('accout', views_message.as_view())
]

# path('entry', views_plan_entry.api_entry),
