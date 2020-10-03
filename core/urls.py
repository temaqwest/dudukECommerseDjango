from django.urls import path
from .views import (
    itemView,
    ItemDetailView,
    checkout,
    add_to_cart,
    remove_from_cart,
    OrderSummaryView
)

app_name = 'core'

urlpatterns = [
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', checkout, name='products'),
    path('', itemView.as_view(), name='item-list'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),

]
