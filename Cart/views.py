from django.shortcuts import get_object_or_404 
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from .serializers import CartItemSerializer, CartItemUpdateSerializer, AddressSerializer, CreateAddressSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied

from .models import Cart, CartItem, Address
from Storefront.models import Product

class CartItemAPI(ListCreateAPIView):
	serializer_class = CartItemSerializer

	def get_queryset(self):
		user = self.request.user
		queryset = CartItem.objects.filter(cart__user=user)
		return queryset

	def create(self, request, *args, **kwargs):
		user = request.user 
		cart = get_object_or_404(Cart, user=user)
		product = get_object_or_404(Product, pk=request.data['Product'])
		current_item = CartItem.objects.filter(cart=cart, Product=product)
		if current_item.count()>0:
			raise NotAcceptable('item already in cart')
		try:
			quantity = int(request.data['quantity'])
		except Exception as e:
			raise ValidationError('please enter your quantity')
		if quantity>product.quantity:
			raise NotAcceptable('ordered quantity more than available')
		else:
			product.quantity-=quantity
		cart_item = CartItem(cart=cart, Product=product, quantity=quantity)
		cart_item.save()
		serializer=CartItemSerializer(cart_item)
		total = float(product.price)*float(quantity)
		cart.total = total
		cart.save()
		return Response( serializer.data, status=status.HTTP_201_CREATED)

class CartItemFunctions(RetrieveUpdateDestroyAPIView):
	serializer_class = CartItemSerializer
	queryset = CartItem.objects.all()
	def retrieve(self, request, *args, **kwargs):
		cart_item = self.get_object()
		if cart_item.cart.user != request.user:
			raise PermissionDenied('this cart does not belong to you')
		serializer = self.get_serializer(cart_item)
		return Response(serializer.data, status=status.HTTP_200_OK)
	def update(self, request, *args, **kwargs):
		cart_item = self.get_object()
		print(request.data)
		product = get_object_or_404(Product, pk=request.data['Product'])
		if cart_item.cart.user != request.user:
			raise PermissionDenied('this cart does not belong to you ')
		try:
			quantity = int(request.data['quantity'])
		except Exception as e:
			raise ValidationError('please, input valid quantity')
		if quantity > product.quantity:
			raise NotAcceptable('order quantity more than available')
		else:
			product.quantity-=quantity

		serializer = CartItemUpdateSerializer(cart_item, data=request.data)
		serializer.is_valid(raise_exception = True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	def destroy(self, request, *args, **kwargs):
		cart_item = self.get_object()
		if cart_item.cart.user != request.user:
			raise PermissionDenied('this cart does not belong to you ')
		cart_item.delete()
		return Response({'detail': 'item has been deleted.'}, status=status.HTTP_204_NO_CONTENT)

class ListAddressAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.filter(user=user)
        return queryset


class AddressDetailView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        address = self.get_object()
        if address.user != user:
            raise NotAcceptable("this address don't belong to you")
        serializer = self.get_serializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)


class createAddressAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateAddressSerializer
    queryset = ""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, primary=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
