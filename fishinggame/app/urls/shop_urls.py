from django.urls import path
from .. import views
from ..shop_view import ShopListView, ShopPurchaseView

# urlpatterns = [
#     path('list/', views.shop_list, name='shop_list'),
#     path('purchase/', views.shop_purchase, name='shop_purchase'),
# ]

urlpatterns = [
    path('list/', ShopListView.as_view(), name='shop_list'),
    path('purchase/', ShopPurchaseView.as_view(), name='shop_purchase'),
]

