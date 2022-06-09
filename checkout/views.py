from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from Storefront.models import Product
from Storefront.serializers import ProductSerializer
from Cart.models import Address
from Cart.serializers import AddressSerializer
from Cart.models import Cart, CartItem
from Cart.serializers import CartItemMiniSerializer

class CheckoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        address_id = request.data.get("address")
        ecommerce_feez = 150
        user_address = Address.objects.filter(id=address_id, user=user)
        product = get_object_or_404(Product, pk=pk)
        total = ecommerce_feez + (product.price * product.quantity)
        data = {}
        data["address"] = AddressSerializer(user_address).data
        data["product"] = ProductSerializer(
            product, context={"request": request}
        ).data
        data["feez"] = ecommerce_feez
        data["total"] = total

        return Response(data, status=status.HTTP_200_OK)


class CheckoutCartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        address_id = request.data.get("address")
        ecommerce_feez = 150
        data = {}
        total = 0
        quantity = 0
        user_address = Address.objects.filter(id=address_id, user=user)
        cart = get_object_or_404(Cart, user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            total += item.Product.price
            quantity += item.quantity
        end_total = ecommerce_feez + (total * quantity)

        data["address"] = AddressSerializer(user_address).data
        data["items"] = CartItemMiniSerializer(cart_items, many=True).data
        data["total"] = end_total
        data["feez"] = ecommerce_feez
        return Response(data, status=status.HTTP_200_OK)