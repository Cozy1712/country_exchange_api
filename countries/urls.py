from django.urls import path
from .views import RefreshCountriesView, CountryListView, CountryDetailView, StatusView, SummaryImageView, CountryView



urlpatterns = [    
    path('countries/refresh', RefreshCountriesView.as_view(), name='refresh_countries'),
    path('countries', CountryListView.as_view(), name='country_list'),
    path('countries/image', SummaryImageView.as_view(), name='get_summary_image'),
    path('status', StatusView.as_view(), name='status'),
    path('countries/<str:name>', CountryDetailView.as_view(), name='country_detail'),
]