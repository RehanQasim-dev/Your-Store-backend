from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.LikedItem)
class CustomerAdmin(admin.ModelAdmin):
    pass