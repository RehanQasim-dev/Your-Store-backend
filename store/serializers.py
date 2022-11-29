from itertools import product
from django.db import transaction
from rest_framework import serializers
from decimal import Decimal
from likes.models import LikedItem
from django.contrib.contenttypes.models import ContentType
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, ProductImage, Review
from django.db.models import Count
from .signals import order_created
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','product','description','username','date']
    product=serializers.PrimaryKeyRelatedField(read_only=True)
    username=serializers.CharField(source='user.username',read_only=True)
    def create(self, validated_data):
        user_id=self.context['user_id']
        product_id=self.context['product_id']
        return Review.objects.create(**validated_data,user_id=user_id,product_id=product_id)

        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['id','phone','birth_date','user','membership','name']
        read_only_fields=['membership']
    name=serializers.SerializerMethodField(method_name='namerakho')
    
class MinimalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','price']
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','description',"inventory",'price','slug','tax','collection','likes','reviews']
    tax=serializers.SerializerMethodField(method_name='calculate_tax')
    likes=serializers.SerializerMethodField(method_name='get_likes')
    reviews=ReviewSerializer(many=True)
    def get_likes(self,product):
        content_type=ContentType.objects.get_for_model(model=Product)
        return LikedItem.objects.filter(content_type=content_type,object_id=product.id).count()
        


    def calculate_tax(self,product):
         return product.price*Decimal(0.1)
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title',"count"]
    # count=serializers.ReadOnlyField(source="product_set.count")
    count=serializers.SerializerMethodField(method_name="Total_Products")
    def Total_Products(self,collection:Collection):
        return collection.product_set.count()

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','cart','quantity',"product",'total_price']
    product=MinimalProductSerializer()
    total_price=serializers.SerializerMethodField(method_name="total_prices")
    def total_prices(self,item:CartItem):
        return item.quantity*item.product.price
class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['product']
class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','product',"product_item","quantity"]
        extra_kwargs={'product':{'write_only':True}}
    
    product_item=MinimalProductSerializer(source='product',read_only=True)
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            return serializers.ValidationError(f"Product with id {value} does not exist.")
        else:
            return value
    def create(self, validated_data):
        return CartItem.objects.create(cart_id=self.context['cart_id'],**validated_data)
    def save(self,**kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product']
        quantity=self.validated_data['quantity']
        try:
            self.instance=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            self.instance.quantity+=quantity
            self.instance.save()
            return self.instance

        except CartItem.DoesNotExist:
            # self.instance=self.create(self.validated_data)
            self.create(self.validated_data)
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=["id",'created_at','items','total']
    total=serializers.SerializerMethodField(method_name='totals',read_only=True)
    def totals(self,cart:Cart):
        return sum([i.quantity*i.product.price for i in cart.items.all()])
    id=serializers.UUIDField(read_only=True)#here in the table
                                                        #field name is id
    items=CartItemSerializer(many=True,read_only=True)

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#             model=Customer
#             fields=['id','full_name','phone','birth_date','user_id']
#             read_only_fields=['full_name']
#     user_id=serializers.IntegerField(read_only=True)#dont know why it is not showing
#                                     #up without this
class CustomerSerializer_me(serializers.ModelSerializer):
    class Meta:
            model=Customer
            fields=['phone','birth_date']
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=['id','product','order','unit_price']
    product=ProductSerializer()
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['id','placed_at','customer','order_status','items','cart_id','message','address','payment_method']
        read_only_fields=['customer','order_status']
        #read_only_fields=['items']#this works only if the field name exists in the model
    items=OrderItemSerializer(many=True,source='psp',read_only=True)#important remember the source
    cart_id=serializers.UUIDField(write_only=True)
    def validate_cart_id(self,value):
        if not Cart.objects.filter(id=value).exists():
            raise serializers.ValidationError('No Cart exists for this id')
        elif CartItem.objects.filter(cart_id=value).count()==0:
            raise serializers.ValidationError('Cart is empty')
        else:
            return value
    def create(self,validated_data):
        with transaction.atomic():
            userid=self.context['user_id']
            print('user id=  ',userid)
            cartid=validated_data['cart_id']
            print('user id=  ',userid)
            _customer=Customer.objects.get(user__id=userid)
            instance=Order.objects.create(customer=_customer)
            orderitems=[OrderItem(product=item.product,unit_price=item.product.price,quantity=item.quantity,order=instance) for item in CartItem.objects.filter(cart_id=cartid)]
            OrderItem.objects.bulk_create(objs=orderitems)
            # Cart.objects.get(id=cartid).delete()
            order_created.send_robust(self.__class__,order=instance)
            return instance
# class OrderSerializerCreate(serializers.ModelSerializer):
#     class Meta:
#         model=Order
#         fields=['cart_id']
#     cart_id=serializers.UUIDField(write_only=True)
class OrderSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['order_status']

    # cart_id=serializers.SerializerMethodField(method_name='test')
    # def test(self,xyz):
    #     self.is_valid(raise_exception=True)#cannot use because data is not yet passed
    #     return self.validated_data['cart_id']
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['image']
    def create(self, validated_data):
        return ProductImage.objects.create(product_id=self.context['product_id'],**validated_data)








