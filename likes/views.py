from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework import mixins
from .models import *
from .Serializers import *
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class ViewSetLikedProducts(    mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class=LikedItemSerializer
    permission_classes=[IsAuthenticated]
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    
                