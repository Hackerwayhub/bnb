# listings/urls.py
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Home page - lists all properties
    path('', views.listing_list, name='home'),

    # Location-specific listings
    path('location/<str:location_slug>/', views.listing_list, name='listings_by_location'),

    # Submit new listing (now requires authentication)
    path('advertise/', views.submit_listing, name='advertise_bnb'),

    # User listing management (all require authentication)
    path('my-listings/', views.my_listings, name='my_bnb_listings'),
    path('edit/<int:listing_id>/', views.edit_listing, name='edit_bnb_listing'),
    path('delete/<int:listing_id>/', views.delete_listing, name='delete_listing'),


    # Individual listing detail
    path('listing/<slug:slug>/', views.listing_detail, name='listing_detail'),

    # Booking pages
    path('book/<int:listing_id>/', views.booking_view, name='booking_form'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),

    # WhatsApp booking
    path('book-via-whatsapp/', views.book_via_whatsapp, name='whatsapp_booking'),

    # Special pages
    path('bnb-house-party/', TemplateView.as_view(template_name='listings/bnb_house_party.html'), name='house_party'),

    # Keep legacy URLs for backward compatibility
    path('submit-listing/', views.submit_listing, name='submit_listing'),  # Legacy - redirects to advertise/
]