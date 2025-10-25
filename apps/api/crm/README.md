# CRM Apps Directory

This directory contains Django apps for core CRM functionality.

## Planned Apps

### contacts
Contact management system
- Contact model with full profile data
- Contact lifecycle tracking
- Activity history
- Custom fields support

### companies
Company/Organization management
- Company profiles
- Hierarchical relationships
- Industry categorization
- Company size and metadata

### deals
Sales pipeline and deal tracking
- Deal stages and pipeline
- Value and probability tracking
- Deal ownership
- Activity association

### activities
Activity tracking system
- Calls, emails, meetings, notes
- Activity timeline
- Activity types and outcomes
- Integration with external systems

### tasks
Task management
- Task creation and assignment
- Due dates and priorities
- Task completion tracking
- Reminders and notifications

## Creating New Apps

```bash
# Inside Docker container
docker-compose exec api python manage.py startapp <app_name>

# Or locally
cd apps/api
python manage.py startapp <app_name>
```

## App Structure

Each app should follow this structure:
```
app_name/
├── __init__.py
├── admin.py          # Django admin configuration
├── apps.py           # App configuration
├── models.py         # Database models
├── serializers.py    # DRF serializers
├── views.py          # API views
├── urls.py           # URL routing
├── tests.py          # Unit tests
├── permissions.py    # Custom permissions
└── migrations/       # Database migrations
```

## Best Practices

1. Keep models focused and single-purpose
2. Use serializers for validation and data transformation
3. Implement proper permissions and authentication
4. Write comprehensive tests
5. Document API endpoints
6. Use signals for cross-app communication
7. Add open collaboration comments for complex logic
