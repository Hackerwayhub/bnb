from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from .models import Listing


# ============================================================================
# STATIC / MARKETING PAGES
# ============================================================================

class StaticSitemap(Sitemap):
    """Sitemap for static public marketing pages."""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return [
            'home',
            'advertise_bnb',
            'whatsapp_booking',
            # NOTE: login, register, password_reset are blocked in robots.txt
            #       and MUST NOT be in the sitemap (causes Search Console warnings).
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()

    def priority(self, item):
        if item == 'home':
            return 1.0
        if item in ['advertise_bnb', 'whatsapp_booking']:
            return 0.9
        return 0.8


# ============================================================================
# PRODUCT LANDING PAGES
# ============================================================================

class ProductSitemap(Sitemap):
    """Sitemap for the product / service landing pages present in urls.py."""
    changefreq = 'weekly'
    priority = 0.95

    def items(self):
        return [
            'safari_landing',
            'invest_landing',
            'bnb_faq',
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()

    def priority(self, item):
        if item in ['safari_landing', 'invest_landing']:
            return 0.95
        if item == 'bnb_faq':
            return 0.75
        return 0.85


# ============================================================================
# LOCATION PAGES
# ============================================================================

class LocationSitemap(Sitemap):
    """Sitemap for every location landing page."""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return [code for code, name in Listing.LOCATIONS]

    def location(self, location_code):
        return reverse(
            'listings_by_location',
            kwargs={'location_slug': location_code.lower()},
        )

    def lastmod(self, location_code):
        latest = Listing.objects.filter(
            location=location_code, is_approved=True
        ).order_by('-updated_at').first()
        return latest.updated_at if latest else None

    def priority(self, location_code):
        count = Listing.objects.filter(
            location=location_code, is_approved=True
        ).count()
        if count > 50:
            return 0.9
        if count > 20:
            return 0.8
        if count > 5:
            return 0.7
        return 0.6


# ============================================================================
# LISTINGS
# ============================================================================

class ListingSitemap(Sitemap):
    """Sitemap for every approved listing detail page."""
    changefreq = 'weekly'
    priority = 0.75

    def items(self):
        return Listing.objects.filter(is_approved=True).order_by('-created_at')

    def location(self, listing):
        return reverse('listing_detail', kwargs={'slug': listing.slug})

    def lastmod(self, listing):
        return listing.updated_at

    def priority(self, listing):
        if listing.listing_type == 'featured':
            return 0.9
        days = (timezone.now() - listing.updated_at).days
        if days < 7:
            return 0.85
        if days < 30:
            return 0.75
        return 0.65


# ============================================================================
# PROPERTY TYPE PAGES
# ============================================================================

class PropertyTypeSitemap(Sitemap):
    """Sitemap for every property type filter page."""
    changefreq = 'weekly'
    priority = 0.75

    def items(self):
        return [code for code, name in Listing.PROPERTY_TYPES]

    def location(self, property_code):
        return reverse(
            'listings_by_property_type',
            kwargs={'property_type_slug': property_code},
        )

    def lastmod(self, property_code):
        latest = Listing.objects.filter(
            property_type=property_code, is_approved=True
        ).order_by('-updated_at').first()
        return latest.updated_at if latest else None

    def priority(self, property_code):
        count = Listing.objects.filter(
            property_type=property_code, is_approved=True
        ).count()
        if count > 50:
            return 0.85
        if count > 20:
            return 0.75
        if count > 5:
            return 0.65
        return 0.55


# ============================================================================
# LISTING TYPE FILTERS (Free / Featured)
# ============================================================================

class ListingTypeSitemap(Sitemap):
    """Sitemap for listing type filter pages (free / featured)."""
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return [code for code, name in Listing.LISTING_TYPE_CHOICES]

    def location(self, listing_type):
        return f"{reverse('home')}?listing_type={listing_type}"

    def lastmod(self, listing_type):
        latest = Listing.objects.filter(
            listing_type=listing_type, is_approved=True
        ).order_by('-updated_at').first()
        return latest.updated_at if latest else None


# ============================================================================
# TRANSACTION TYPE FILTERS (Rent / Sale / Shortlet)
# ============================================================================

class TransactionTypeSitemap(Sitemap):
    """Sitemap for transaction type filter pages (rent / sale / shortlet)."""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return [code for code, name in Listing.TRANSACTION_TYPE_CHOICES]

    def location(self, transaction_type):
        return f"{reverse('home')}?transaction_type={transaction_type}"

    def lastmod(self, transaction_type):
        latest = Listing.objects.filter(
            transaction_type=transaction_type, is_approved=True
        ).order_by('-updated_at').first()
        return latest.updated_at if latest else None


# ============================================================================
# USER PAGES
# ============================================================================

class UserSitemap(Sitemap):
    """Sitemap for user-facing pages (auth-required, low priority)."""
    changefreq = 'monthly'
    priority = 0.3

    def items(self):
        return ['my_bnb_listings']

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()


# ============================================================================
# MASTER SITEMAP DICT
# ============================================================================

sitemaps = {
    'static': StaticSitemap,
    'products': ProductSitemap,
    'locations': LocationSitemap,
    'listings': ListingSitemap,
    'property_types': PropertyTypeSitemap,
    'listing_types': ListingTypeSitemap,
    'transaction_types': TransactionTypeSitemap,
    'user_pages': UserSitemap,
}