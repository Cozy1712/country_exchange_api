from django.contrib import admin
from .models import Country
# Register your models here.


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'currency_code', 'exchange_rate', 'estimated_gdp')
    search_fields = ('name', 'currency_code', 'region')