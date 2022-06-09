from django.urls import path
from . import views 
urlpatterns = [
	path('cart/', views.CartItemAPI.as_view()),
	path('cart-item/<int:pk>/', views.CartItemFunctions.as_view()),
    path("addresses/", views.ListAddressAPIView.as_view()),
    path("address/<int:pk>", views.AddressDetailView.as_view()),
    path("create/address/", views.createAddressAPIView.as_view()),
	
]