from itertools import product
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *



from store.models import Product
from django.contrib.contenttypes.models import ContentType
class LikedItemSerializer(ModelSerializer):
    class Meta:
        model=LikedItem
        fields=['id','product_id']
        extra_kwargs={'product_id':{'write_only':True}}
    product_id=serializers.IntegerField(write_only=True)
    def create(self,validated_data):
        user_id=self.context['user_id']
        print(validated_data)
        product_id=validated_data['product_id']
        # content_object=Product.objects.get(id=product_id)
        content_type_object=ContentType.objects.get_for_model(model=Product)
        return LikedItem.objects.create(user_id=user_id,content_type=content_type_object,object_id=product_id)
       


