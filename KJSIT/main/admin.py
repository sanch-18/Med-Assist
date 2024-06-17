from django.contrib import admin

# Register your models here.
from .models import Person, Contact_info, History

admin.site.register(Person)
admin.site.register(Contact_info)
admin.site.register(History)