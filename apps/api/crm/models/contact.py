"""
Contact Model - Individual People

This model represents individual people in the CRM.
Lives in TENANT SCHEMAS (isolated per tenant).

A Contact is:
- A person with contact information (email, phone)
- Can belong to an Organization (company they work for)
- Has a lifecycle stage (Lead → Prospect → Customer, etc.)
- Tracks ownership (which user manages this contact)
- Records timestamps and custom fields

Examples:
- John Doe, CEO at Acme Corp
- Jane Smith, Marketing Manager at TechStart
- Bob Johnson, Independent Consultant
"""

import uuid
from django.db import models
from django.conf import settings


class Contact(models.Model):
    """
    Contact Model (Tenant-specific)
    
    Represents an individual person in the CRM.
    Each tenant has their own contacts table with isolated data.
    
    Relationships:
    - Belongs to one Organization (optional)
    - Owned by one User (who manages this contact)
    - Has many Activities (calls, emails, meetings)
    - Has many Deals (sales opportunities)
    - Has many Tasks (to-do items)
    - Has many Notes (free-form notes)
    
    Usage:
        # Create a contact
        contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='+1234567890',
            lifecycle_stage='lead',
            owner=request.user
        )
    """
    
    # Lifecycle stages - how far along the sales process
    LIFECYCLE_STAGES = [
        ('subscriber', 'Subscriber'),           # Newsletter subscriber
        ('lead', 'Lead'),                       # Initial interest
        ('marketing_qualified', 'Marketing Qualified Lead (MQL)'),
        ('sales_qualified', 'Sales Qualified Lead (SQL)'),
        ('opportunity', 'Opportunity'),         # Active sales process
        ('customer', 'Customer'),               # Closed-won
        ('evangelist', 'Evangelist'),           # Promoter/advocate
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this contact"
    )
    
    # Basic Information
    first_name = models.CharField(
        max_length=100,
        help_text="Contact's first name"
    )
    
    last_name = models.CharField(
        max_length=100,
        help_text="Contact's last name"
    )
    
    email = models.EmailField(
        unique=True,
        help_text="Primary email address"
    )
    
    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Primary phone number"
    )
    
    mobile = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Mobile phone number"
    )
    
    # Professional Information
    job_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Job title (e.g., 'CEO', 'Marketing Manager')"
    )
    
    # Organization relationship
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contacts',
        help_text="Company this contact works for"
    )
    
    # Lifecycle & Status
    lifecycle_stage = models.CharField(
        max_length=50,
        choices=LIFECYCLE_STAGES,
        default='lead',
        help_text="Where this contact is in the sales process"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Is this contact active? Inactive contacts are hidden from most views"
    )
    
    # Ownership & Assignment
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_contacts',
        help_text="User who owns/manages this contact"
    )
    
    # Additional Contact Details
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
        help_text="Apartment, suite, etc."
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
    
    # Social Media & Web
    linkedin_url = models.URLField(
        blank=True,
        null=True,
        help_text="LinkedIn profile URL"
    )
    
    twitter_handle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Twitter/X handle (without @)"
    )
    
    website = models.URLField(
        blank=True,
        null=True,
        help_text="Personal website"
    )
    
    # Notes & Description
    description = models.TextField(
        blank=True,
        null=True,
        help_text="General notes about this contact"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this contact was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this contact was last updated"
    )
    
    last_contacted = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When we last contacted this person"
    )
    
    # Lead Source
    lead_source = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=[
            ('website', 'Website'),
            ('referral', 'Referral'),
            ('linkedin', 'LinkedIn'),
            ('email_campaign', 'Email Campaign'),
            ('event', 'Event/Conference'),
            ('cold_outreach', 'Cold Outreach'),
            ('partner', 'Partner'),
            ('other', 'Other'),
        ],
        help_text="How did this contact find us?"
    )
    
    class Meta:
        db_table = 'contacts'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['lifecycle_stage']),
            models.Index(fields=['owner']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.get_full_name()
    
    def get_full_name(self):
        """
        Returns the contact's full name
        Example: "John Doe"
        """
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_display_name(self):
        """
        Returns name with job title if available
        Example: "John Doe, CEO"
        """
        name = self.get_full_name()
        if self.job_title:
            return f"{name}, {self.job_title}"
        return name
    
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
