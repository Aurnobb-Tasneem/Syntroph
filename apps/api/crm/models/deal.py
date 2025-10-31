"""
Deal Model - Sales Opportunities

This model represents sales opportunities/deals in the CRM.
Lives in TENANT SCHEMAS (isolated per tenant).

A Deal is:
- A sales opportunity with a monetary value
- Goes through pipeline stages (Prospecting → Closed Won/Lost)
- Belongs to an Organization (company being sold to)
- Has a Contact (primary person at the org)
- Tracked by an owner (sales rep managing the deal)
- Has expected close date and probability

Examples:
- "Enterprise License Deal" - $50,000 - Acme Corp
- "Consulting Services" - $25,000 - TechStart Inc
- "Annual Subscription" - $12,000 - Big Company LLC
"""

import uuid
from django.db import models
from django.conf import settings
from decimal import Decimal


class Deal(models.Model):
    """
    Deal Model (Tenant-specific)
    
    Represents a sales opportunity in the CRM.
    Each tenant has their own deals table with isolated data.
    
    Relationships:
    - Belongs to one Organization (company)
    - Has one primary Contact (decision maker)
    - Owned by one User (sales rep)
    - Has many Activities (calls, emails, meetings)
    - Has many Tasks (follow-ups)
    - Has many Notes
    
    Usage:
        # Create a deal
        deal = Deal.objects.create(
            name='Enterprise License',
            organization=acme_corp,
            contact=john_doe,
            amount=50000.00,
            stage='negotiation',
            probability=75,
            expected_close_date='2025-12-31',
            owner=sales_rep
        )
    """
    
    # Deal stages in sales pipeline
    STAGES = [
        ('lead', 'Lead'),
        ('qualified', 'Qualified'),
        ('meeting_scheduled', 'Meeting Scheduled'),
        ('proposal_sent', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]
    
    # Loss reasons (why deals are lost)
    LOSS_REASONS = [
        ('price', 'Price Too High'),
        ('competitor', 'Lost to Competitor'),
        ('timing', 'Bad Timing'),
        ('budget', 'No Budget'),
        ('no_decision', 'No Decision'),
        ('requirements', 'Requirements Not Met'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this deal"
    )
    
    # Basic Information
    name = models.CharField(
        max_length=255,
        help_text="Deal name (e.g., 'Enterprise License Q4 2025')"
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of the deal"
    )
    
    # Financial Information
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Deal value in USD"
    )
    
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="Currency code (USD, EUR, GBP, etc.)"
    )
    
    # Relationships
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='deals',
        help_text="Company this deal is with"
    )
    
    contact = models.ForeignKey(
        'Contact',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deals',
        help_text="Primary contact for this deal"
    )
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_deals',
        help_text="Sales rep who owns this deal"
    )
    
    # Pipeline & Status
    stage = models.CharField(
        max_length=50,
        choices=STAGES,
        default='lead',
        help_text="Current stage in the sales pipeline"
    )
    
    probability = models.IntegerField(
        default=0,
        help_text="Win probability (0-100%)"
    )
    
    expected_close_date = models.DateField(
        null=True,
        blank=True,
        help_text="When we expect to close this deal"
    )
    
    actual_close_date = models.DateField(
        null=True,
        blank=True,
        help_text="When the deal was actually closed"
    )
    
    # Loss Information (for closed_lost deals)
    loss_reason = models.CharField(
        max_length=50,
        choices=LOSS_REASONS,
        blank=True,
        null=True,
        help_text="Why was this deal lost?"
    )
    
    loss_reason_detail = models.TextField(
        blank=True,
        null=True,
        help_text="Additional details about why deal was lost"
    )
    
    # Additional Fields
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
            ('inbound', 'Inbound'),
            ('other', 'Other'),
        ],
        help_text="How did this opportunity originate?"
    )
    
    next_step = models.TextField(
        blank=True,
        null=True,
        help_text="What's the next action for this deal?"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this deal was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this deal was last updated"
    )
    
    class Meta:
        db_table = 'deals'
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['stage']),
            models.Index(fields=['organization']),
            models.Index(fields=['owner']),
            models.Index(fields=['expected_close_date']),
            models.Index(fields=['-amount']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.organization.name} (${self.amount:,.2f})"
    
    def is_open(self):
        """Check if deal is still open (not won or lost)"""
        return self.stage not in ['closed_won', 'closed_lost']
    
    def is_won(self):
        """Check if deal was won"""
        return self.stage == 'closed_won'
    
    def is_lost(self):
        """Check if deal was lost"""
        return self.stage == 'closed_lost'
    
    def mark_as_won(self, close_date=None):
        """Mark deal as won"""
        from django.utils import timezone
        self.stage = 'closed_won'
        self.probability = 100
        self.actual_close_date = close_date or timezone.now().date()
        self.save()
    
    def mark_as_lost(self, reason=None, reason_detail=None, close_date=None):
        """Mark deal as lost"""
        from django.utils import timezone
        self.stage = 'closed_lost'
        self.probability = 0
        self.loss_reason = reason
        self.loss_reason_detail = reason_detail
        self.actual_close_date = close_date or timezone.now().date()
        self.save()
    
    @property
    def weighted_value(self):
        """
        Calculate weighted value (amount * probability)
        Used for pipeline forecasting
        """
        return Decimal(str(self.amount)) * Decimal(self.probability / 100)
    
    @property
    def days_to_close(self):
        """
        Calculate days until expected close date
        Negative if overdue
        """
        if not self.expected_close_date:
            return None
        
        from django.utils import timezone
        delta = self.expected_close_date - timezone.now().date()
        return delta.days
    
    @property
    def is_overdue(self):
        """Check if deal is past expected close date"""
        days = self.days_to_close
        return days is not None and days < 0 and self.is_open()
