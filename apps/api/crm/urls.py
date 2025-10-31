"""
CRM URL Configuration

Maps API endpoints to ViewSets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from crm.views import ContactViewSet, OrganizationViewSet, DealViewSet

# Create a router and register our ViewSets
router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'deals', DealViewSet, basename='deal')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
