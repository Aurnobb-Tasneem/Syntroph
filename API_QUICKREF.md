# Syntroph CRM API Quick Reference

## Server
```bash
# Start Django server
cd d:\Syntroph\apps\api
python manage.py runserver
```

## Authentication
Currently accessible without authentication (will add JWT in next phase).

## Tenant Routing
Add tenant ID header to all requests:
```bash
-H "X-Tenant-ID: <tenant-uuid>"
```

## Endpoints

### Contacts

#### List Contacts
```bash
curl http://127.0.0.1:8000/api/contacts/
```

#### Create Contact
```bash
curl -X POST http://127.0.0.1:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0100",
    "job_title": "CEO",
    "lifecycle_stage": "customer"
  }'
```

#### Get Contact
```bash
curl http://127.0.0.1:8000/api/contacts/<contact-id>/
```

#### Update Contact
```bash
curl -X PATCH http://127.0.0.1:8000/api/contacts/<contact-id>/ \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1-555-0199"}'
```

#### Delete Contact
```bash
curl -X DELETE http://127.0.0.1:8000/api/contacts/<contact-id>/
```

#### Search Contacts
```bash
# Search by name, email, phone, job title
curl "http://127.0.0.1:8000/api/contacts/?search=john"

# Filter by lifecycle stage
curl "http://127.0.0.1:8000/api/contacts/?lifecycle_stage=lead"

# Filter by organization
curl "http://127.0.0.1:8000/api/contacts/?organization=<org-id>"

# Order by created date
curl "http://127.0.0.1:8000/api/contacts/?ordering=-created_at"
```

#### Recent Contacts
```bash
curl http://127.0.0.1:8000/api/contacts/recent/
```

#### Group by Lifecycle Stage
```bash
curl http://127.0.0.1:8000/api/contacts/by_lifecycle_stage/
```

---

### Organizations

#### List Organizations
```bash
curl http://127.0.0.1:8000/api/organizations/
```

#### Create Organization
```bash
curl -X POST http://127.0.0.1:8000/api/organizations/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corporation",
    "domain": "acme.com",
    "industry": "technology",
    "employee_count": "51-200",
    "annual_revenue": "5000000.00",
    "lifecycle_stage": "customer"
  }'
```

#### Get Organization
```bash
curl http://127.0.0.1:8000/api/organizations/<org-id>/
```

#### Update Organization
```bash
curl -X PATCH http://127.0.0.1:8000/api/organizations/<org-id>/ \
  -H "Content-Type: application/json" \
  -d '{"annual_revenue": "6000000.00"}'
```

#### Delete Organization
```bash
curl -X DELETE http://127.0.0.1:8000/api/organizations/<org-id>/
```

#### Get Organization Contacts
```bash
curl http://127.0.0.1:8000/api/organizations/<org-id>/contacts/
```

#### Get Organization Deals
```bash
curl http://127.0.0.1:8000/api/organizations/<org-id>/deals/
```

#### Get Organization Stats
```bash
curl http://127.0.0.1:8000/api/organizations/<org-id>/stats/
```

#### Search Organizations
```bash
# Search by name, domain
curl "http://127.0.0.1:8000/api/organizations/?search=acme"

# Filter by industry
curl "http://127.0.0.1:8000/api/organizations/?industry=technology"

# Filter by employee count
curl "http://127.0.0.1:8000/api/organizations/?employee_count=51-200"
```

---

### Deals

#### List Deals
```bash
curl http://127.0.0.1:8000/api/deals/
```

#### Create Deal
```bash
curl -X POST http://127.0.0.1:8000/api/deals/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Enterprise License Deal",
    "amount": "150000.00",
    "currency": "USD",
    "stage": "proposal_sent",
    "probability": 75,
    "organization": "<org-id>",
    "contact": "<contact-id>",
    "expected_close_date": "2025-12-31",
    "description": "Annual enterprise software license"
  }'
```

#### Get Deal
```bash
curl http://127.0.0.1:8000/api/deals/<deal-id>/
```

#### Update Deal
```bash
curl -X PATCH http://127.0.0.1:8000/api/deals/<deal-id>/ \
  -H "Content-Type: application/json" \
  -d '{"stage": "negotiation", "probability": 85}'
```

#### Delete Deal
```bash
curl -X DELETE http://127.0.0.1:8000/api/deals/<deal-id>/
```

#### Mark Deal as Won
```bash
curl -X POST http://127.0.0.1:8000/api/deals/<deal-id>/mark_won/
```

#### Mark Deal as Lost
```bash
curl -X POST http://127.0.0.1:8000/api/deals/<deal-id>/mark_lost/ \
  -H "Content-Type: application/json" \
  -d '{"reason": "Chose competitor"}'
```

#### Search Deals
```bash
# Search by name, description
curl "http://127.0.0.1:8000/api/deals/?search=enterprise"

# Filter by stage
curl "http://127.0.0.1:8000/api/deals/?stage=proposal_sent"

# Filter by organization
curl "http://127.0.0.1:8000/api/deals/?organization=<org-id>"

# Order by amount
curl "http://127.0.0.1:8000/api/deals/?ordering=-amount"
```

#### Group by Stage
```bash
curl http://127.0.0.1:8000/api/deals/by_stage/
```

#### Pipeline Statistics
```bash
curl http://127.0.0.1:8000/api/deals/pipeline/
```

#### Overdue Deals
```bash
curl http://127.0.0.1:8000/api/deals/overdue/
```

---

## Response Formats

### Contact List Response
```json
[
  {
    "id": "uuid",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0100",
    "job_title": "CEO",
    "organization_name": "Acme Corporation",
    "lifecycle_stage": "customer",
    "owner_name": "Admin User",
    "created_at": "2025-11-01T05:00:00Z"
  }
]
```

### Organization Detail Response
```json
{
  "id": "uuid",
  "name": "Acme Corporation",
  "domain": "acme.com",
  "industry": "technology",
  "employee_count": "51-200",
  "annual_revenue": "5000000.00",
  "lifecycle_stage": "customer",
  "owner_name": "Admin User",
  "contact_count": 5,
  "deal_count": 3,
  "total_deal_value": 450000.0,
  "contacts": [
    { "id": "uuid", "full_name": "John Doe", "email": "john.doe@example.com" }
  ],
  "created_at": "2025-11-01T05:00:00Z",
  "updated_at": "2025-11-01T05:00:00Z"
}
```

### Deal Detail Response
```json
{
  "id": "uuid",
  "name": "Enterprise License Deal",
  "amount": "150000.00",
  "currency": "USD",
  "stage": "proposal_sent",
  "probability": 75,
  "organization_name": "Acme Corporation",
  "contact_name": "John Doe",
  "owner_name": "Admin User",
  "expected_close_date": "2025-12-31",
  "actual_close_date": null,
  "weighted_value": 112500.0,
  "days_to_close": 60,
  "is_overdue": false,
  "is_open": true,
  "is_won": false,
  "is_lost": false,
  "created_at": "2025-11-01T05:00:00Z",
  "updated_at": "2025-11-01T05:00:00Z"
}
```

### Pipeline Statistics Response
```json
{
  "total_deals": 10,
  "open_deals": 7,
  "won_deals": 2,
  "lost_deals": 1,
  "total_value": 1250000.0,
  "total_weighted_value": 875000.0,
  "won_value": 300000.0,
  "win_rate": 20.0
}
```

---

## Filter & Search Options

### Contacts
- **Search**: first_name, last_name, email, phone, mobile, job_title
- **Filters**: lifecycle_stage, organization, owner
- **Ordering**: created_at, updated_at, first_name, last_name

### Organizations
- **Search**: name, domain, phone, email
- **Filters**: industry, employee_count, lifecycle_stage, owner
- **Ordering**: created_at, updated_at, name, annual_revenue

### Deals
- **Search**: name, description
- **Filters**: stage, organization, contact, owner
- **Ordering**: created_at, updated_at, amount, expected_close_date, probability

---

## Enum Values

### Contact Lifecycle Stages
- `subscriber`
- `lead`
- `marketing_qualified_lead` (MQL)
- `sales_qualified_lead` (SQL)
- `opportunity`
- `customer`
- `evangelist`

### Deal Stages
- `lead`
- `qualified`
- `meeting_scheduled`
- `proposal_sent`
- `negotiation`
- `closed_won`
- `closed_lost`

### Industries
- `technology`
- `finance`
- `healthcare`
- `education`
- `retail`
- `manufacturing`
- `real_estate`
- `professional_services`
- `non_profit`
- `other`

### Employee Count Ranges
- `1-10`
- `11-50`
- `51-200`
- `201-500`
- `501-1000`
- `1001-5000`
- `5001-10000`
- `10001+`

---

## Testing Script

```bash
# Run API structure validation
cd d:\Syntroph\apps\api
python test_api_structure.py
```

---

## Common Workflows

### Create a Complete Deal
```bash
# 1. Create Organization
ORG_ID=$(curl -X POST http://127.0.0.1:8000/api/organizations/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corp", "domain": "acme.com"}' \
  | jq -r '.id')

# 2. Create Contact
CONTACT_ID=$(curl -X POST http://127.0.0.1:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d "{\"first_name\": \"John\", \"last_name\": \"Doe\", \"email\": \"john@acme.com\", \"organization\": \"$ORG_ID\"}" \
  | jq -r '.id')

# 3. Create Deal
curl -X POST http://127.0.0.1:8000/api/deals/ \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Q4 Enterprise Deal\",
    \"amount\": \"250000\",
    \"stage\": \"qualified\",
    \"probability\": 60,
    \"organization\": \"$ORG_ID\",
    \"contact\": \"$CONTACT_ID\",
    \"expected_close_date\": \"2025-12-31\"
  }"
```

---

**Last Updated**: November 1, 2025  
**Django Server**: http://127.0.0.1:8000  
**API Base**: http://127.0.0.1:8000/api/
