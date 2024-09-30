from django.urls import path

from . import views
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    path('api-token-auth/', rest_views.obtain_auth_token),
    path('me/', views.CurrentUserView.as_view()),
    path('cards/', views.GetCardInfoView.as_view()),
    path('free-coins/', views.free_coins),
    path('combine/', views.Combine.as_view()),
    path('buy/', views.BuyRandom.as_view()),
    path('destroy/', views.Destroy.as_view()),
    path('shop/list', views.ShopList.as_view()),
    path('shop/buy', views.ShopBuyCard.as_view()),
]