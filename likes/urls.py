from django.urls import path
from . import views
from rest_framework_nested import routers
router1=routers.DefaultRouter()
router1.register('liked_items',viewset=views.ViewSetLikedProducts,basename='liked_items')
urlpatterns=router1.urls