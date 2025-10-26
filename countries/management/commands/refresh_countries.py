import random , requests
from django.core.management.base import BaseCommand
from django.conf import settings
from countries.models import Country
from countries.utils.image_generator import generate_summary_image
# from django.db import transaction
from datetime import datetime
from django.utils import timezone




COUNTRIES_URL = settings.RESTCOUNTRIES_URL 
EXCHANGE_URL = settings.EXCHANGE_RATE_URL 

def do_refresh():
    """
    Reusable helper to refresh countries and exchange rate data.
    Returns total number of countries refreshed.
    Used by both API view and Django management command.
    """
    # COUNTRIES_URL = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
    # EXCHANGE_URL = " https://open.er-api.com/v6/latest/USD"

    # Fetch countries
    countries_res = requests.get(COUNTRIES_URL, timeout=20)
    countries_res.raise_for_status()
    countries_data = countries_res.json()

    # Fetch exchange rates
    rates_res = requests.get(EXCHANGE_URL, timeout=20)
    rates_res.raise_for_status()
    rates_data = rates_res.json()
    exchange_rates = rates_data.get("rates", {})

    count = 0
    for country in countries_data:
        name = country.get("name")
        if not name:
            continue

        capital = country.get("capital")
        region = country.get("region")
        population = country.get("population") or 0
        flag_url = country.get("flag")

        currencies = country.get("currencies") or []
        currency_code = None
        exchange_rate = None
        estimated_gdp = 0.0

        if currencies:
            currency_code = currencies[0].get("code") if currencies[0] else None

        if currency_code:
            exchange_rate = exchange_rates.get(currency_code)
            if exchange_rate:
                multiplier = random.randint(1000, 2000)
                estimated_gdp = (population * multiplier) / exchange_rate
            else:
                estimated_gdp = None

        Country.objects.update_or_create(
            name__iexact=name,
            defaults={
                "name": name,
                "capital": capital,
                "region": region,
                "population": population,
                "currency_code": currency_code,
                "exchange_rate": exchange_rate,
                "estimated_gdp": estimated_gdp,
                "flag_url": flag_url,
                "last_refreshed_at": timezone.now(),
            },
        )
        count += 1

    # Optional — regenerate the summary image
    try:
        generate_summary_image()
    except Exception:
        pass  # Skip silently if utils not implemented yet

    return count



# --- DJANGO MANAGEMENT COMMAND ---
class Command(BaseCommand):
    help = "Fetch all countries and exchange rates, then cache them in the database"

    def handle(self, *args, **options):
        self.stdout.write("Fetching country and exchange rate data...")
        try:
            total = do_refresh()
            self.stdout.write(self.style.SUCCESS(f"Refresh complete. {total} countries updated."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed: {e}"))
            raise SystemExit(1)
