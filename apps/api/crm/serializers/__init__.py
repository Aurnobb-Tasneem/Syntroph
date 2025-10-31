"""
CRM Serializers

Transform Django models to/from JSON for API responses.
"""

from rest_framework import serializers
from crm.models import Contact, Organization, Deal
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing contacts
    Only includes essential fields for performance
    """
    owner_name = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'job_title', 'organization_name', 'lifecycle_stage',
            'owner_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_owner_name(self, obj):
        return obj.owner.get_full_name() if obj.owner else None
    
    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class ContactDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for contact details
    Includes all fields and related data
    """
    owner_name = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    full_address = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_owner_name(self, obj):
        return obj.owner.get_full_name() if obj.owner else None
    
    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_display_name(self, obj):
        return obj.get_display_name()
    
    def get_full_address(self, obj):
        return obj.full_address


class OrganizationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing organizations
    """
    owner_name = serializers.SerializerMethodField()
    contact_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'domain', 'industry', 'employee_count',
            'lifecycle_stage', 'owner_name', 'contact_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_owner_name(self, obj):
        return obj.owner.get_full_name() if obj.owner else None
    
    def get_contact_count(self, obj):
        return obj.get_contact_count()


class OrganizationDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for organization details
    """
    owner_name = serializers.SerializerMethodField()
    contact_count = serializers.SerializerMethodField()
    deal_count = serializers.SerializerMethodField()
    total_deal_value = serializers.SerializerMethodField()
    full_address = serializers.SerializerMethodField()
    contacts = ContactListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_owner_name(self, obj):
        return obj.owner.get_full_name() if obj.owner else None
    
    def get_contact_count(self, obj):
        return obj.get_contact_count()
    
    def get_deal_count(self, obj):
        return obj.get_deal_count()
    
    def get_total_deal_value(self, obj):
        return float(obj.get_total_deal_value())
    
    def get_full_address(self, obj):
        return obj.full_address


class DealListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing deals
    """
    owner_name = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()
    contact_name = serializers.SerializerMethodField()
    weighted_value = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Deal
        fields = [
            'id', 'name', 'amount', 'currency', 'stage', 'probability',
            'organization_name', 'contact_name', 'owner_name',
            'expected_close_date', 'weighted_value', 'is_overdue', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_owner_name(self, obj):
        return obj.owner.get_full_name() if obj.owner else None
    
    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None
    
    def get_contact_name(self, obj):
        return obj.contact.get_full_name() if obj.contact else None
    
    def get_weighted_value(self, obj):
        return float(obj.weighted_value)
    
    def get_is_overdue(self, obj):
        return obj.is_overdue


class DealDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for deal details
    """
    owner_name = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()
    contact_name = serializers.SerializerMethodField()
    weighted_value = serializers.SerializerMethodField()
    days_to_close = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()
    is_won = serializers.SerializerMethodField()
    is_lost = serializers.SerializerMethodField()
    
    class Meta:
        model = Deal
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_owner_name(self, obj):
        return obj.owner.get_full_name() if obj.owner else None
    
    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None
    
    def get_contact_name(self, obj):
        return obj.contact.get_full_name() if obj.contact else None
    
    def get_weighted_value(self, obj):
        return float(obj.weighted_value)
    
    def get_days_to_close(self, obj):
        return obj.days_to_close
    
    def get_is_overdue(self, obj):
        return obj.is_overdue
    
    def get_is_open(self, obj):
        return obj.is_open()
    
    def get_is_won(self, obj):
        return obj.is_won()
    
    def get_is_lost(self, obj):
        return obj.is_lost()
