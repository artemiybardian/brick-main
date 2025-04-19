from django.contrib import admin
from authen.models import CustomUser, Country, City


admin.site.register(CustomUser)
admin.site.register(Country)
admin.site.register(City)
