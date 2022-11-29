from django.shortcuts import render
from djoser.views import UserViewSet as uvs
from djoser.conf import settings
from .models import User
# Create your views here.

class UserViewSet(uvs):
    pass
    # def get_queryset(self):
    #     if self.action=='me':
    #         return User.objects.select_related('customer').all()
    #     user = self.request.user
    #     queryset = super().get_queryset()
    #     if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
    #         queryset = queryset.filter(pk=user.pk)
    #     return queryset