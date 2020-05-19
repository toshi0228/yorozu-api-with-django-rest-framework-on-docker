from django.urls import path, include
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
router.register('account', views_account.AccountViewSet)
router.register('profile', views_profile.ProfileViewSet)
router.register('plan', views_plan.PlanViewSet)
router.register('tag', views_tag.TagViewSet)
router.register('message', views_message.MessageViewSet)
router.register('review', views_review.MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('accout', views_message.as_view())
]

# path('entry', views_plan_entry.api_entry),
