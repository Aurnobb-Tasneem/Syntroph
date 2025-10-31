"""
CRM ViewSets

REST API endpoints for CRM models with tenant isolation.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from crm.models import Contact, Organization, Deal
from crm.serializers import (
    ContactListSerializer,
    ContactDetailSerializer,
    OrganizationListSerializer,
    OrganizationDetailSerializer,
    DealListSerializer,
    DealDetailSerializer,
)


class TenantAccessPermission(IsAuthenticated):
    """
    Custom permission to ensure user has access to the tenant.
    Combined with TenantPermissionMiddleware for defense-in-depth.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not super().has_permission(request, view):
            return False
        
        # Tenant verification is already handled by middleware
        # This is an additional check for defense-in-depth
        return hasattr(request, 'tenant') and request.tenant is not None


class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing contacts.
    
    Provides:
    - list: List all contacts in current tenant
    - create: Create a new contact
    - retrieve: Get a specific contact
    - update: Update a contact (PUT)
    - partial_update: Partially update a contact (PATCH)
    - destroy: Delete a contact
    - search: Search contacts by name, email, phone
    - by_lifecycle_stage: Filter contacts by lifecycle stage
    """
    queryset = Contact.objects.all()
    permission_classes = [TenantAccessPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['lifecycle_stage', 'organization', 'owner']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'mobile', 'job_title']
    ordering_fields = ['created_at', 'updated_at', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for list vs detail views"""
        if self.action == 'list':
            return ContactListSerializer
        return ContactDetailSerializer
    
    def perform_create(self, serializer):
        """Set the owner to the current user when creating a contact"""
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_lifecycle_stage(self, request):
        """Group contacts by lifecycle stage"""
        stages = {}
        for stage_key, stage_label in Contact.LIFECYCLE_STAGES:
            contacts = self.queryset.filter(lifecycle_stage=stage_key)
            stages[stage_key] = {
                'label': stage_label,
                'count': contacts.count(),
                'contacts': ContactListSerializer(contacts[:10], many=True).data
            }
        return Response(stages)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recently created contacts"""
        contacts = self.queryset.order_by('-created_at')[:20]
        serializer = ContactListSerializer(contacts, many=True)
        return Response(serializer.data)


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing organizations.
    
    Provides:
    - list: List all organizations in current tenant
    - create: Create a new organization
    - retrieve: Get a specific organization
    - update: Update an organization (PUT)
    - partial_update: Partially update an organization (PATCH)
    - destroy: Delete an organization
    - contacts: Get all contacts for an organization
    - deals: Get all deals for an organization
    - stats: Get statistics for an organization
    """
    queryset = Organization.objects.all()
    permission_classes = [TenantAccessPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['industry', 'employee_count', 'lifecycle_stage', 'owner']
    search_fields = ['name', 'domain', 'phone', 'email']
    ordering_fields = ['created_at', 'updated_at', 'name', 'annual_revenue']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for list vs detail views"""
        if self.action == 'list':
            return OrganizationListSerializer
        return OrganizationDetailSerializer
    
    def perform_create(self, serializer):
        """Set the owner to the current user when creating an organization"""
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def contacts(self, request, pk=None):
        """Get all contacts for this organization"""
        organization = self.get_object()
        contacts = organization.contacts.all()
        serializer = ContactListSerializer(contacts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def deals(self, request, pk=None):
        """Get all deals for this organization"""
        organization = self.get_object()
        deals = organization.deals.all()
        serializer = DealListSerializer(deals, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for this organization"""
        organization = self.get_object()
        return Response({
            'contact_count': organization.get_contact_count(),
            'deal_count': organization.get_deal_count(),
            'total_deal_value': float(organization.get_total_deal_value()),
        })


class DealViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing deals.
    
    Provides:
    - list: List all deals in current tenant
    - create: Create a new deal
    - retrieve: Get a specific deal
    - update: Update a deal (PUT)
    - partial_update: Partially update a deal (PATCH)
    - destroy: Delete a deal
    - by_stage: Group deals by stage
    - pipeline: Get pipeline statistics
    - mark_won: Mark a deal as won
    - mark_lost: Mark a deal as lost
    - overdue: Get overdue deals
    """
    queryset = Deal.objects.all()
    permission_classes = [TenantAccessPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['stage', 'organization', 'contact', 'owner']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'amount', 'expected_close_date', 'probability']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for list vs detail views"""
        if self.action == 'list':
            return DealListSerializer
        return DealDetailSerializer
    
    def perform_create(self, serializer):
        """Set the owner to the current user when creating a deal"""
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_stage(self, request):
        """Group deals by stage"""
        stages = {}
        for stage_key, stage_label in Deal.STAGE_CHOICES:
            deals = self.queryset.filter(stage=stage_key)
            total_value = sum(float(deal.amount) for deal in deals)
            stages[stage_key] = {
                'label': stage_label,
                'count': deals.count(),
                'total_value': total_value,
                'deals': DealListSerializer(deals[:10], many=True).data
            }
        return Response(stages)
    
    @action(detail=False, methods=['get'])
    def pipeline(self, request):
        """Get pipeline statistics"""
        total_deals = self.queryset.count()
        open_deals = self.queryset.filter(
            stage__in=['lead', 'qualified', 'meeting_scheduled', 'proposal_sent', 'negotiation']
        )
        won_deals = self.queryset.filter(stage='closed_won')
        lost_deals = self.queryset.filter(stage='closed_lost')
        
        total_value = sum(float(deal.amount) for deal in open_deals)
        total_weighted_value = sum(float(deal.weighted_value) for deal in open_deals)
        won_value = sum(float(deal.amount) for deal in won_deals)
        
        return Response({
            'total_deals': total_deals,
            'open_deals': open_deals.count(),
            'won_deals': won_deals.count(),
            'lost_deals': lost_deals.count(),
            'total_value': total_value,
            'total_weighted_value': total_weighted_value,
            'won_value': won_value,
            'win_rate': won_deals.count() / max(total_deals, 1) * 100,
        })
    
    @action(detail=True, methods=['post'])
    def mark_won(self, request, pk=None):
        """Mark a deal as won"""
        deal = self.get_object()
        deal.mark_as_won()
        serializer = self.get_serializer(deal)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_lost(self, request, pk=None):
        """Mark a deal as lost"""
        deal = self.get_object()
        reason = request.data.get('reason', '')
        deal.mark_as_lost(reason)
        serializer = self.get_serializer(deal)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue deals"""
        deals = [deal for deal in self.queryset if deal.is_overdue]
        serializer = DealListSerializer(deals, many=True)
        return Response(serializer.data)
