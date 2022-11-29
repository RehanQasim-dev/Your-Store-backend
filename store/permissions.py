from django.http import HttpRequest
from rest_framework.permissions import BasePermission,DjangoModelPermissions
from rest_framework import permissions

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request:HttpRequest, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
class CustomModelPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET']=['%(app_label)s.add_%(model_name)s']
class IsAdminOrAuthRead(BasePermission):
    def has_permission(self, request:HttpRequest, view):
        if  request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        elif request.user.is_staff:
            return True
        else:
            return False
class IsAdminOrAuthPOST(BasePermission):
    def has_permission(self, request:HttpRequest, view):
        if  request.method=='POST' and request.user.is_authenticated:
            return True
        elif request.user.is_staff:
            return True
        else:
            return False
