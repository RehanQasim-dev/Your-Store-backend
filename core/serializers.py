from djoser.serializers import UserCreateSerializer as ucs,UserSerializer as us
from numpy import source
from .models import User
from rest_framework import serializers

class UserCreateSerializer(ucs):
    class Meta(ucs.Meta):
        Model=User
        fields = ['id','email','username','first_name','last_name','password']
        # read_only_fields=['last_name']
    # first_name=serializers.CharField(read_only=True)
    password=serializers.CharField(style={'input_type':'password'},write_only=True)
class UserSerializer(us):
    class Meta(us.Meta):
        fields=['id','username','first_name','last_name','email','birthdate']
    birthdate=serializers.SerializerMethodField(method_name='ello')
    def ello(self,user:User):
        # if user==0:
        #     return None
        return user.customer.all()[0].birth_date