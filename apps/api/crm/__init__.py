"""
CRM App - Customer Relationship Management

This Django app contains all CRM-related models, services, and APIs.

Models (Tenant-specific data):
- Contact: Individual people
- Organization: Companies/businesses
- Deal: Sales opportunities
- Activity: Interactions (calls, emails, meetings)
- Task: To-do items
- Note: Free-form notes

These models live in TENANT SCHEMAS, not the public schema.
Each tenant has their own isolated copy of these tables.
"""
