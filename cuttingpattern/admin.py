from django.contrib import admin

from .models import User, CuttingPattern, Customer, CustomerGroup

# Register your models here.
admin.site.register(User)
admin.site.register(CuttingPattern)
admin.site.register(CustomerGroup)
admin.site.register(Customer)
