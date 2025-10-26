from rest_framework import serializers
from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            'id', 'name', 'capital', 'region', 'population',
            'currency_code', 'exchange_rate', 'estimated_gdp',
            'flag_url', 'last_refreshed_at',
        ]

    def validate(self, data):
        errors = {}
        if 'name' not in data or not data.get('name'):
            errors['name'] = 'is required'
        if 'population' in data:
            if data.get('population') is None:
                errors['population'] = 'is required'
        else:
            errors['population'] = 'is required'
        # currency_code required on user create/update via API (refresh may set null)
        if self.instance is None and not data.get('currency_code'):
            errors['currency_code'] = 'is required'


        if errors:
            raise serializers.ValidationError({
                'error': 'Validation failed', 'details': errors
            })
        return data