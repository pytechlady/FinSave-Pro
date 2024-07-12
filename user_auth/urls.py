from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_auth.views import *


router = DefaultRouter()
router.register(r'', UserAuthenticationViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
]