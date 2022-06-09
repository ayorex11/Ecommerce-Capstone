from rest_framework import serializers
from .models import Cart, CartItem, Address
from Storefront.models import Product


class CartProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('category', 'name', 'description', 'price', 'available')


class CartItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem 
		fields = ['cart', 'Product', 'quantity']

class CartItemMiniSerializer(serializers.ModelSerializer):
	Product = CartProductSerializer(required=False)

	class Meta:
		model = CartItem
		fields = ['Product', 'quantity']


class CartItemUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields = ['Product', 'quantity']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['country', 'city', 'user', 'district', 'street_address', 'postal_code', 'building_number', 'apartment_number']


class CreateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["primary", "user"]