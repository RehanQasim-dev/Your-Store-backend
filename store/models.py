
from email import message
from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator
from core.models import User
from django.conf import settings
from django.contrib import admin
from .Validators import image_validator,Title_validator
class Product(models.Model):
    title=models.CharField(max_length=255)
    slug=models.CharField(max_length=255,null=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=6,decimal_places=2,validators=[MinValueValidator(1,message="aqal kr ly kuch")])
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey('Collection',on_delete=models.PROTECT)
    promotion=models.ManyToManyField("Promotion")
    def __str__(self) -> str:
        return self.title
class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='store/images',validators=[image_validator])
class Customer(models.Model):
    memb_choices=[("B","Bronze"),("G","Gold"),("S","Silver")]
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='customer',unique=True)
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1,choices=memb_choices,default="B")
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    def full_name(self):
        return self.first_name()+self.last_name()
    def __str__(self) -> str:
        return self.user.first_name+self.user.last_name
class Order(models.Model):
    order_status=[("P","Pending"),("C","Complete"),("F","Failed")]
    payment_method=[("Cash On Delivery",'Cash On Delivery'),("Via JazzCash/EasyPaisa","Via JazzCash/EasyPaisa"),('Online Bank Transfer','Online Bank Transfer')]
    address=models.TextField(max_length=255)
    message=models.TextField(max_length=255,default='')
    placed_at=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(max_length=1,choices=order_status,default="P")
    payment_method=models.CharField(max_length=255,choices=payment_method,default='Cash On Delivery')
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)
class Address(models.Model):
    city=models.CharField(max_length=255)
    street=models.CharField(max_length=255)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)

class Collection(models.Model):
    title=models.CharField(max_length=255,validators=[Title_validator])
    featured_product=models.ForeignKey("Product",on_delete=models.SET_NULL,
    null=True,related_name="+")
    def __str__(self) -> str:
        return self.title

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='psp')
    quantity=models.PositiveIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)

class Cart(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid4)
    created_at=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    quantity=models.PositiveIntegerField()
    class Meta:
        unique_together=[['product','cart']]
    # def __str__(self) -> str:
    #     return self.product
class Promotion(models.Model):
    description=models.TextField(blank=True)
    def __str__(self) -> str:
        return self.description
class Review(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    description=models.TextField()
    date=models.DateTimeField(auto_now_add=True)






