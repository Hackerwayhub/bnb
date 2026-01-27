# listings/urls.py
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Home page - lists all properties
    path('', views.listing_list, name='home'),

    # Submit new listing
    path('submit-listing/', views.submit_listing, name='submit_listing'),
    path('location/<str:location_slug>/', views.listing_list, name='listings_by_location'),
    path('book-on-whatsapp/', views.book_via_whatsapp, name='whatsapp_booking'),

path('book/<int:listing_id>/', views.booking_view, name='booking_form'),
#
    path('bnb-house-party/', TemplateView.as_view(template_name='BNBHOUSEPARTY.html'), name='house_party'),

]