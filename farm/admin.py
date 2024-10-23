from django.contrib import admin

# Register your models here.

from farm.models import Farm, Property

admin.site.register([Farm, Property])
