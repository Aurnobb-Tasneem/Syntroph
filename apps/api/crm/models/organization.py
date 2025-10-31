"""
Organization Model - Companies/Businesses

This model represents companies or organizations in the CRM.
Lives in TENANT SCHEMAS (isolated per tenant).

An Organization is:
- A company or business entity
- Has many Contacts (people who work there)
- Has many Deals (sales opportunities with this company)
- Tracks company details (industry, size, revenue)
- Records ownership and lifecycle

Examples:
- Acme Corporation (Technology, 500 employees)
- TechStart Inc (Startup, 10 employees)
- Big Enterprise LLC (Manufacturing, 5000 employees)
"""

import uuid
from django.db import models
from django.conf import settings


class Organization(models.Model):
    """
    Organization Model (Tenant-specific)
    
    Represents a company or business in the CRM.
    Each tenant has their own organizations table with isolated data.
    
    Relationships:
    - Has many Contacts (employees)
    - Has many Deals (sales opportunities)
    - Owned by one User (who manages this organization)
    - Has many Activities, Tasks, Notes
    
    Usage:
        # Create an organization
        org = Organization.objects.create(
            name='Acme Corporation',
            industry='technology',
            employee_count='51-200',
            annual_revenue=5000000,
            owner=request.user
        )
    """
    
    # Industry choices
    INDUSTRIES = [
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('manufacturing', 'Manufacturing'),
        ('retail', 'Retail'),
        ('education', 'Education'),
        ('real_estate', 'Real Estate'),
        ('consulting', 'Consulting'),
        ('media', 'Media & Entertainment'),
        ('transportation', 'Transportation'),
        ('energy', 'Energy'),
        ('telecommunications', 'Telecommunications'),
        ('hospitality', 'Hospitality'),
        ('other', 'Other'),
    ]
    
    # Employee count ranges
    EMPLOYEE_COUNTS = [
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1001-5000', '1001-5000 employees'),
        ('5001+', '5001+ employees'),
    ]
    
    # Lifecycle stages for organizations
    LIFECYCLE_STAGES = [
        ('lead', 'Lead'),
        ('qualified', 'Qualified'),
        ('opportunity', 'Opportunity'),
        ('customer', 'Customer'),
        ('evangelist', 'Evangelist'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this organization"
    )
    
    # Basic Information
    name = models.CharField(
        max_length=255,
        help_text="Company name"
    )
    
    domain = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Company website domain (e.g., 'acme.com')"
    )
    
    industry = models.CharField(
        max_length=50,
        choices=INDUSTRIES,
        blank=True,
        null=True,
        help_text="Company industry"
    )
    
    employee_count = models.CharField(
        max_length=20,
        choices=EMPLOYEE_COUNTS,
        blank=True,
        null=True,
        help_text="Number of employees"
    )
    
    annual_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Annual revenue in USD"
    )
    
    # Contact Information
    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Main phone number"
    )
    
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="General contact email"
    )
    
    website = models.URLField(
        blank=True,
        null=True,
        help_text="Company website"
    )
    
    # Address
    address_line1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Street address"
    )
    
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Suite, floor, etc."
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="City"
    )
    
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="State/Province"
    )
    
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="ZIP/Postal code"
    )
    
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Country"
    )
    
    # Lifecycle & Status
    lifecycle_stage = models.CharField(
        max_length=50,
        choices=LIFECYCLE_STAGES,
        default='lead',
        help_text="Where this organization is in the sales process"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Is this organization active?"
    )
    
    # Ownership
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_organizations',
        help_text="User who owns/manages this organization"
    )
    
    # Social Media
    linkedin_url = models.URLField(
        blank=True,
        null=True,
        help_text="LinkedIn company page"
    )
    
    twitter_handle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Twitter/X handle (without @)"
    )
    
    # Notes & Description
    description = models.TextField(
        blank=True,
        null=True,
        help_text="General notes about this organization"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this organization was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this organization was last updated"
    )
    
    last_contacted = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When we last contacted this organization"
    )
    
    class Meta:
        db_table = 'organizations'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['domain']),
            models.Index(fields=['industry']),
            models.Index(fields=['lifecycle_stage']),
            models.Index(fields=['owner']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def full_address(self):
        """
        Returns formatted full address
        """
        parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            f"{self.state} {self.postal_code}".strip(),
            self.country
        ]
        return ', '.join([p for p in parts if p])
    
    def get_contact_count(self):
        """
        Returns number of contacts at this organization
        """
        return self.contacts.count()
    
    def get_deal_count(self):
        """
        Returns number of deals with this organization
        """
        return self.deals.count()
    
    def get_total_deal_value(self):
        """
        Returns total value of all deals with this organization
        """
        from django.db.models import Sum
        total = self.deals.aggregate(total=Sum('amount'))['total']
        return total or 0
