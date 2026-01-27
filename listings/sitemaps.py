from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Listing


class StaticSitemap(Sitemap):
    """Sitemap for static pages"""
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return ['home', 'submit_listing', 'whatsapp_booking', 'house_party']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        # Home page gets highest priority
        if item == 'home':
            return 1.0
        # WhatsApp booking page gets high priority too
        elif item == 'whatsapp_booking':
            return 0.9
        elif item == 'house_party':
            return 0.8
        return 0.7

    def lastmod(self, item):
        # For static pages, we can return a recent date
        from django.utils import timezone
        return timezone.now()


class LocationSitemap(Sitemap):
    """Sitemap for all location pages based on your LOCATIONS choices"""
    changefreq = 'weekly'
    priority = 0.7

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

    def lastmod(self, obj):
        # Get the latest listing update for this location
        latest_listing = Listing.objects.filter(
            location=obj,
            is_approved=True
        ).order_by('-updated_at').first()

        if latest_listing:
            return latest_listing.updated_at
        return None


class ListingSitemap(Sitemap):
    """Sitemap for individual listing pages (if you have detail views)"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        # Only include approved listings
        return Listing.objects.filter(is_approved=True).order_by('-created_at')

    def location(self, obj):
        # If you have individual listing detail pages, use:
        # return reverse('listing_detail', kwargs={'slug': obj.slug})

        # For now, since you don't have detail pages, link to home
        # Or you could link to the location page
        return reverse('home')

    def lastmod(self, obj):
        return obj.updated_at


# Combine all sitemaps
sitemaps = {
    'static': StaticSitemap,
    'locations': LocationSitemap,
    'listings': ListingSitemap,
}