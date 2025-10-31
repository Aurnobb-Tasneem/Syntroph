from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TenantSignUpForm
from .models import Client, Domain

def tenant_signup_view(request):
    if request.method == 'POST':
        form = TenantSignUpForm(request.POST)
        if form.is_valid():
            tenant = form.save(commit=False)
            tenant.save()  # auto_create_schema=True → creates schema automatically

            domain = Domain()
            domain.domain = f"{tenant.schema_name}.localhost"  # for local dev
            domain.tenant = tenant
            domain.is_primary = True
            domain.save()

            messages.success(request, f"Tenant '{tenant.name}' created successfully!")
            return redirect('tenant_signup')
        else:
            messages.error(request, "There were errors in your form.")
    else:
        form = TenantSignUpForm()

    return render(request, 'tenant_signup.html', {'form': form})

