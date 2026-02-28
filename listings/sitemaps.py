from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Listing
from django.utils import timezone


class StaticSitemap(Sitemap):
    """Sitemap for static pages"""
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return [
            'home',  # Main homepage
            'advertise_bnb',  # Submit listing page
            'whatsapp_booking',  # WhatsApp booking page
            'all_property_types',  # Property types overview page
            'login',  # Login page
            'register',  # Registration page
            'password_reset',  # Password reset page
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        # Home page gets highest priority
        if item == 'home':
            return 1.0
        # Important pages get high priority
        elif item in ['advertise_bnb', 'whatsapp_booking']:
            return 0.9
        elif item == 'all_property_types':
            return 0.8
        # Auth pages
        elif item in ['login', 'register']:
            return 0.7
        return 0.6

    def lastmod(self, item):
        # For static pages, return current time
        return timezone.now()


class LocationSitemap(Sitemap):
    """Sitemap for all location pages with clean URLs"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        # Get all location choices from your model
        location_choices = Listing.LOCATIONS
        # Extract just the location codes
        location_codes = [code for code, name in location_choices]
        return location_codes

    def location(self, location_code):
        # Convert location code to slug format
        location_slug = location_code.lower()
        return reverse('listings_by_location', kwargs={'location_slug': location_slug})

    def lastmod(self, location_code):
        # Get the latest listing update for this location
        latest_listing = Listing.objects.filter(
            location=location_code,
            is_approved=True
        ).order_by('-updated_at').first()

        if latest_listing:
            return latest_listing.updated_at
        return None

    def priority(self, location_code):
        # Higher priority for locations with more listings
        count = Listing.objects.filter(location=location_code, is_approved=True).count()
        if count > 50:
            return 0.9
        elif count > 20:
            return 0.8
        elif count > 5:
            return 0.7
        return 0.6


class ListingSitemap(Sitemap):
    """Sitemap for individual listing pages"""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        # Only include approved listings
        return Listing.objects.filter(
            is_approved=True
        ).order_by('-created_at')

    def location(self, listing):
        return reverse('listing_detail', kwargs={'slug': listing.slug})

    def lastmod(self, listing):
        return listing.updated_at

    def priority(self, listing):
        # Give higher priority to featured listings
        if listing.listing_type == 'featured':
            return 0.9
        # Higher priority to recently updated listings
        days_since_update = (timezone.now() - listing.updated_at).days
        if days_since_update < 7:
            return 0.8
        elif days_since_update < 30:
            return 0.7
        return 0.6


class PropertyTypeSitemap(Sitemap):
    """Sitemap for property type pages with clean URLs"""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        # Get all property type choices from your model
        return [code for code, name in Listing.PROPERTY_TYPES]

    def location(self, property_code):
        # Create clean URL with the property type code (with underscore)
        # Your URLs use underscore: /property-type/rent_studio/
        return reverse('listings_by_property_type', kwargs={'property_type_slug': property_code})

    def lastmod(self, property_code):
        # Get the latest listing update for this property type
        latest_listing = Listing.objects.filter(
            property_type=property_code,
            is_approved=True
        ).order_by('-updated_at').first()

        if latest_listing:
            return latest_listing.updated_at
        return None

    def priority(self, property_code):
        # Higher priority for property types with more listings
        count = Listing.objects.filter(property_type=property_code, is_approved=True).count()
        if count > 50:
            return 0.8
        elif count > 20:
            return 0.7
        elif count > 5:
            return 0.6
        return 0.5


class PropertyTypeOverviewSitemap(Sitemap):
    """Sitemap for the all property types overview page"""
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return ['all_property_types']

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()


class ListingTypeSitemap(Sitemap):
    """Sitemap for listing type filter pages (free/featured)"""
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return [code for code, name in Listing.LISTING_TYPE_CHOICES]

    def location(self, listing_type):
        # Create URL with query parameter for listing type
        base_url = reverse('home')
        return f"{base_url}?listing_type={listing_type}"

    def lastmod(self, listing_type):
        latest_listing = Listing.objects.filter(
            listing_type=listing_type,
            is_approved=True
        ).order_by('-updated_at').first()

        if latest_listing:
            return latest_listing.updated_at
        return None


class TransactionTypeSitemap(Sitemap):
    """Sitemap for transaction type filter pages (Rent, Sale, Shortlet)"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return [code for code, name in Listing.TRANSACTION_TYPE_CHOICES]

    def location(self, transaction_type):
        # Create URL with query parameter for transaction type
        base_url = reverse('home')
        return f"{base_url}?transaction_type={transaction_type}"

    def lastmod(self, transaction_type):
        latest_listing = Listing.objects.filter(
            transaction_type=transaction_type,
            is_approved=True
        ).order_by('-updated_at').first()

        if latest_listing:
            return latest_listing.updated_at
        return None


class UserSitemap(Sitemap):
    """Sitemap for user-related pages"""
    changefreq = 'monthly'
    priority = 0.4

    def items(self):
        return [
            'my_bnb_listings',  # User's listings page
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()


# Combine all sitemaps
sitemaps = {
    'static': StaticSitemap,
    'locations': LocationSitemap,
    'listings': ListingSitemap,
    'property_types': PropertyTypeSitemap,  # Clean URLs for each property type
    'property_overview': PropertyTypeOverviewSitemap,  # Overview page of all property types
    'listing_types': ListingTypeSitemap,
    'transaction_types': TransactionTypeSitemap,
    'user_pages': UserSitemap,
}