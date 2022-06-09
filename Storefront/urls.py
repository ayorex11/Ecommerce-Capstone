from django.urls import path
from . import views

urlpatterns = [
	path('categories/', views.category_list ),
	path('products/', views.product_list),
	path('productdetail/<str:pk>/', views.ProductDetail),
]