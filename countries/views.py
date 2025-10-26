from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import FileResponse
from .models import Country
from .serializers import CountrySerializer
from .management.commands.refresh_countries import do_refresh # we'll implement a callable helper
import os

# Create your views here.
class CountryView(APIView):
    def post(self, request):
        serializer = CountrySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # process valid data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RefreshCountriesView(APIView):
    def post(self, request):
        try:
            total = do_refresh()
        except Exception as e:
            return Response({
                'error': 'External data source unavailable',
                'details': str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({
            'message': 'Refresh successful',
            'total_countries': total
        })
        
class CountryListView(generics.ListAPIView):
    serializer_class = CountrySerializer

    def get_queryset(self):
        qs = Country.objects.all()
        region = self.request.query_params.get('region')
        currency = self.request.query_params.get('currency')
        sort = self.request.query_params.get('sort') 
        if region:
            qs = qs.filter(region__iexact=region)
        if currency:
            qs = qs.filter(currency_code__iexact=currency)
        if sort == 'gdp_desc':
            qs = qs.order_by('-estimated_gdp')
        return qs
        
class CountryDetailView(APIView):
    def get(self, request, name):
        country = get_object_or_404(Country, name__iexact = name)
        serializer = CountrySerializer(country)
        return Response(serializer.data)
    
    def delete(self, request, name):
        try:
            country = Country.objects.get(name__iexact=name)
        except Country.DoesNotExist:
            return Response({'error': 'Country not found'}, status=status.HTTP_404_NOT_FOUND)
        country.delete()
        return Response({'message': 'Country deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class StatusView(APIView):
    def get(self, request):
        total = Country.objects.count()
        last = None
        last_obj = Country.objects.order_by('-last_refreshed_at').first()
        if last_obj:
            last = last_obj.last_refreshed_at
        return Response({'total_countries': total, 'last_refreshed_at': last})


class SummaryImageView(APIView):
    def get(self, request):
        path = settings.SUMMARY_IMAGE_PATH
        if not os.path.exists(path):
            return Response({'error': 'Summary image not found'}, status=404)
        return FileResponse(open(path, 'rb'), content_type='image/png')