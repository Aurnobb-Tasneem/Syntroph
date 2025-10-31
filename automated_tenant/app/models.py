from django.db import models
from django.conf import settings
from django_tenants.models import TenantMixin, DomainMixin

# Create your models here.
class Client(TenantMixin): 
  name = models.CharField(max_length=100)
  email = models.EmailField(null=True, blank=True)
  created_on = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)
  industry = models.CharField(max_length=100, null=True, blank=True)
  auto_create_schema = True
  auto_drop_schema = True


  def __str__(self):
        return f"{self.name} ({self.schema_name})"

class Domain(DomainMixin):
  pass 

