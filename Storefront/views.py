from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer, ProductSerializer
from drf_yasg.utils import swagger_auto_schema

from .models import Category, Product

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def category_list(request):
    
    data = Category.objects.all()
    serializer = CategorySerializer(data, many=True)

    data = {'message':'success',
            'data':serializer.data}
    
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def product_list(request):
    
    data = Product.objects.filter(available=True)
    serializer = ProductSerializer(data, many=True)

    data = {'message':'success',
            'data':serializer.data}
    
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def ProductDetail(request, pk):
    
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)