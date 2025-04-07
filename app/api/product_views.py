# views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Cart, CartItem, Order
from .serializers import ProductSerializer, CartSerializer, OrderSerializer
from django.shortcuts import get_object_or_404

# Product Info
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Add to Cart
class AddToCart(APIView):
    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()

        return Response({'message': 'Added to cart'})


# View Cart
class ViewCart(APIView):
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# Checkout
class Checkout(APIView):
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        total = cart.total_price()

        order = Order.objects.create(user=request.user, cart=cart, total=total)

        # Optionally, empty the cart
        cart.items.all().delete()

        return Response({'message': 'Order placed!', 'order_id': order.id})
