from django.db import models
# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=200, unique=True) # match by case-insensitive in code
    capital = models.CharField(max_length=200, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    population = models.BigIntegerField()


    currency_code = models.CharField(max_length=10, null=True, blank=True)
    exchange_rate = models.FloatField(null=True, blank=True) # rate relative to USD
    estimated_gdp = models.FloatField(null=True, blank=True)


    flag_url = models.URLField(null=True, blank=True)
    last_refreshed_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    