from django.urls import path
from .views import ProductList, AddToCart, ViewCart, Checkout

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('cart/add/', AddToCart.as_view(), name='add-to-cart'),
    path('cart/view/', ViewCart.as_view(), name='view-cart'),
    path('checkout/', Checkout.as_view(), name='checkout'),
]