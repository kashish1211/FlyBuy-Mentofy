from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Product(models.Model):
	name = models.CharField(max_length = 100)
	price = models.CharField(max_length = 100)
	description = models.TextField()
	image = models.ImageField(default='default.jpg', upload_to='product_pics')


	def __str__(self):
		return (self.name) 	

	def save(self):
		super().save()

		img = Image.open(self.image.path)
		if img.height > 250 or img.width > 300:
			output_size=(300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)	


class CartItem(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	is_selected = models.BooleanField(default=False)
	quantity = models.IntegerField(default=1)

	def get_total_price(self):
		return self.quantity * int(self.item.price)

	def __str__(self):
		return f"{self.quantity} of {self.item.name}"



class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ManyToManyField(CartItem)
	ordered = models.BooleanField(default=False)
	billing_address = models.ForeignKey('CheckoutInfo',on_delete=models.SET_NULL, blank=True, null=True)


	def __str__(self):
		return (self.user.username)


class CheckoutInfo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	address = models.CharField(max_length=100)
	apartment_address = models.CharField(max_length=100)
	country = CountryField(multiple=False)
	pin = models.CharField(max_length = 100)

	def __str__(self):
		return (self.user.username)
		
        

