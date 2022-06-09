from django.db import models
from Storefront.models import Product 
from django.contrib.auth import get_user_model
from django.dispatch import receiver 
from django.db.models.signals import post_save 
from django_countries.fields import CountryField 
from django.core.validators import MinValueValidator
User = get_user_model()





class TimeStampedModel(models.Model):
	created = models.DateTimeField(db_index=True, auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract=True
	

class Cart(TimeStampedModel):
	user = models.OneToOneField(User, related_name='user_cart', on_delete=models.CASCADE)
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)



@receiver(post_save, sender=User)
def create_cart(sender, created, instance, *args, **kwargs):
	if created:
		Cart.objects.create(user=instance)

class CartItem(TimeStampedModel):
	cart = models.ForeignKey(Cart, related_name='cart_item', on_delete=models.CASCADE)
	Product = models.ForeignKey(Product, related_name='cart_product', on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)


class Address(TimeStampedModel):
    user = models.ForeignKey(User, related_name="address", on_delete=models.CASCADE)
    country = CountryField(blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    district = models.CharField(max_length=100, blank=False, null=False)
    street_address = models.CharField(max_length=250, blank=False, null=False)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    primary = models.BooleanField(default=False)
    
    building_number = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1)]
    )
    apartment_number = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1)]
    )
