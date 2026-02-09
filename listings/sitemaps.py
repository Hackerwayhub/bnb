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
            'home',
            'submit_listing',
            'whatsapp_booking',
            'house_party',
            'login',
            'register',
            'password_reset'
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        # Home page gets highest priority
        if item == 'home':
            return 1.0
        # Important pages get high priority
        elif item == 'whatsapp_booking':
            return 0.9
        elif item == 'submit_listing':
            return 0.85
        elif item == 'house_party':
            return 0.8
        # Auth pages
        elif item in ['login', 'register']:
            return 0.7
        return 0.6

    def lastmod(self, item):
        # For static pages, return current time
        return timezone.now()


class LocationSitemap(Sitemap):
    """Sitemap for all location pages based on your LOCATIONS choices"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        # Get all location choices from your model
        # This returns tuples like ('westlands', 'Westlands')
        location_choices = Listing.LOCATIONS

        # Extract just the location codes (the slugs)
        location_codes = [code for code, name in location_choices]
        return location_codes

    def location(self, location_code):
        # Convert location code to slug format (already lowercase in your case)
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
        # Return the URL for the individual listing detail page
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
    """Sitemap for property type filter pages"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        # Get all property type choices from your model
        return [code for code, name in Listing.PROPERTY_TYPES]

    def location(self, property_type):
        # Create URL with query parameter for property type
        base_url = reverse('home')
        return f"{base_url}?property_type={property_type}"

    def lastmod(self, property_type):
        # Get the latest listing update for this property type
        latest_listing = Listing.objects.filter(
            property_type=property_type,
            is_approved=True
        ).order_by('-updated_at').first()

        if latest_listing:
            return latest_listing.updated_at
        return None


class ListingTypeSitemap(Sitemap):
    """Sitemap for listing type filter pages"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        # Get all listing type choices from your model
        return [code for code, name in Listing.LISTING_TYPE_CHOICES]

    def location(self, listing_type):
        # Create URL with query parameter for listing type
        base_url = reverse('home')
        return f"{base_url}?listing_type={listing_type}"

    def lastmod(self, listing_type):
        # Get the latest listing update for this listing type
        latest_listing = Listing.objects.filter(
            listing_type=listing_type,
            is_approved=True
        ).order_by('-updated_at').first()

        if latest_listing:
            return latest_listing.updated_at
        return None


# Combine all sitemaps
sitemaps = {
    'static': StaticSitemap,
    'locations': LocationSitemap,
    'listings': ListingSitemap,
    'property_types': PropertyTypeSitemap,
    'listing_types': ListingTypeSitemap,
}