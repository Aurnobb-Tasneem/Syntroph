from django.urls import path
from .views import tenant_signup_view

urlpatterns = [
    path('', tenant_signup_view, name='tenant_signup'),
]
