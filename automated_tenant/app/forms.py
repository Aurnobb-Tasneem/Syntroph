from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Client

class TenantSignUpForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'schema_name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Company Name'}),
            'schema_name': forms.TextInput(attrs={'placeholder': 'Subdomain (e.g. bigco)'}),
            'email' : forms.EmailInput(attrs={'placeholder': 'Company Email'}),
        }

    def clean_schema_name(self):
        schema_name = self.cleaned_data['schema_name'].lower()

        if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', schema_name):
            raise ValidationError("Subdomains may contain only lowercase letters, numbers, and hyphens.")

        if Client.objects.filter(schema_name=schema_name).exists():
            raise ValidationError("This subdomain is already taken.")

        return schema_name
