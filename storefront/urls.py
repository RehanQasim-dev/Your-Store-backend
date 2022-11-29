"""first URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from djoser import urls
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
from core.views import UserViewSet
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()
router.register("users", UserViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('store/', include('store.urls')),
    path('auth/', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
    # path('testing/',include('testing.urls'))
    # path('tag/', include('tag.urls')),
    path('likes/', include('likes.urls')),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]