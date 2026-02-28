# listings/views.py
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Case, When, IntegerField
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from .forms import ListingSubmissionForm, BookingForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Listing, Booking
import logging
import urllib.parse

# Set up logger
logger = logging.getLogger(__name__)


# ============================================================================
# HELPER FUNCTIONS - Shared logic for all listing views
# ============================================================================

def get_filtered_listings(request, base_queryset=None, **kwargs):
    """
    Shared filtering logic for all listing views
    """
    if base_queryset is None:
        base_queryset = Listing.objects.filter(is_approved=True)

    # Get filters from request
    location = kwargs.get('location') or request.GET.get('location')
    property_type = kwargs.get('property_type') or request.GET.get('property_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    listing_type = request.GET.get('listing_type', 'all')

    # Apply filters
    if location and location != 'all':
        base_queryset = base_queryset.filter(location=location)
    if property_type:
        base_queryset = base_queryset.filter(property_type=property_type)
    if min_price:
        base_queryset = base_queryset.filter(price_per_night__gte=min_price)
    if max_price:
        base_queryset = base_queryset.filter(price_per_night__lte=max_price)
    if listing_type and listing_type != 'all':
        base_queryset = base_queryset.filter(listing_type=listing_type)

    return base_queryset


def prepare_listing_context(request, queryset, context_extra=None):
    """
    Prepare common context for listing pages (both location and property type)
    This creates all the data needed for listings.html template
    """
    # Generate a random seed based on session or current timestamp
    random_seed = request.session.get('random_seed', random.randint(1, 1000000))
    request.session['random_seed'] = random_seed + 1

    # Convert to list for shuffling
    all_listings = list(queryset)

    # Separate featured and non-featured listings
    featured_listings = [listing for listing in all_listings if listing.listing_type == 'featured']
    non_featured_listings = [listing for listing in all_listings if listing.listing_type != 'featured']

    # Shuffle both lists separately with the current random seed
    random.seed(random_seed)
    random.shuffle(featured_listings)
    random.shuffle(non_featured_listings)

    # Combine: featured first, then non-featured
    all_listings_shuffled = featured_listings + non_featured_listings

    # Pagination
    paginator = Paginator(all_listings_shuffled, 99)  # 12 listings per page for better UX
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get counts
    total_listings = len(all_listings_shuffled)
    featured_count = len(featured_listings)
    free_count = len(non_featured_listings)

    # Get featured listings for slider
    featured_slider_listings = featured_listings[:3]
    if not featured_slider_listings:
        featured_slider_listings = non_featured_listings[:3]

    # Create location data with slugs for template
    all_location_choices = Listing.LOCATIONS
    locations_with_slugs = []
    location_choices_dict = dict(all_location_choices)

    for location_code, loc_display_name in all_location_choices:
        slug = location_code.lower()
        locations_with_slugs.append({
            'code': location_code,
            'name': loc_display_name,
            'slug': slug,
            'url': f'/location/{slug}/'
        })

    # Get property types from model choices
    property_types = Listing.PROPERTY_TYPES

    # Get listing types from model choices
    listing_types = Listing.LISTING_TYPE_CHOICES

    # Base context
    context = {
        'listings': page_obj,
        'page_obj': page_obj,
        'all_locations': locations_with_slugs,
        'location_choices_dict': location_choices_dict,
        'property_types': property_types,
        'listing_types': listing_types,
        'total_listings': total_listings,
        'featured_count': featured_count,
        'free_count': free_count,
        'featured_listings': featured_slider_listings,
        'featured_price': 1000.00,
        'current_filters': {
            'location': request.GET.get('location', 'all'),
            'property_type': request.GET.get('property_type'),
            'listing_type': request.GET.get('listing_type', 'all'),
            'min_price': request.GET.get('min_price'),
            'max_price': request.GET.get('max_price'),
        },
    }

    # Add extra context if provided
    if context_extra:
        context.update(context_extra)

    return context


def get_location_slug_mappings():
    """
    Create mapping between location slugs and codes
    """
    LOCATION_SLUGS = {}
    for location_code, location_display_name in Listing.LOCATIONS:
        slug = location_code.lower()
        LOCATION_SLUGS[slug] = location_code
    return LOCATION_SLUGS

def get_property_type_slug_mappings():
    """
    Create mapping between property type slugs and codes
    Your property_type_slug from URL is 'rent_studio' (with underscore, not hyphen)
    """
    PROPERTY_TYPE_SLUGS = {}
    for code, display_name in Listing.PROPERTY_TYPES:
        # The slug is the same as the code (with underscore)
        # Because your URL is /property-type/rent_studio/ not /property-type/rent-studio/
        slug = code  # Keep the underscore
        PROPERTY_TYPE_SLUGS[slug] = code
    return PROPERTY_TYPE_SLUGS

# ============================================================================
# MAIN LISTING VIEWS - Both use the same listings.html template
# ============================================================================

def listing_list(request, location_slug=None):
    """
    Home page - Display all approved listings or location-specific listings
    Uses listings.html template
    """
    # Get location mappings
    LOCATION_SLUGS = get_location_slug_mappings()
    location_choices_dict = dict(Listing.LOCATIONS)

    # Get selected location from URL slug or query parameter
    if location_slug:
        selected_location = LOCATION_SLUGS.get(location_slug)
        location_specific = True
    else:
        selected_location = request.GET.get('location', 'all')
        location_specific = False

    # Get location name for display
    display_location_name = 'All Locations'
    if selected_location and selected_location != 'all':
        display_location_name = location_choices_dict.get(selected_location, selected_location.title())

    # Get location slug for current location (for template)
    current_location_slug = None
    if selected_location and selected_location != 'all':
        for slug, code in LOCATION_SLUGS.items():
            if code == selected_location:
                current_location_slug = slug
                break

    # Get filtered listings
    queryset = get_filtered_listings(request, location=selected_location)

    # Prepare context
    context_extra = {
        'selected_location': selected_location,
        'selected_listing_type': request.GET.get('listing_type', 'all'),
        'location_name': display_location_name,
        'current_location_slug': current_location_slug,
        'location_specific': location_specific,
        'page_type': 'location',
        'page_title': f'Bnb,staycations,holiday homes &  houses for rent in {display_location_name}! | Bnb.co.ke' if selected_location != 'all' else 'Bnb.co.ke | Bnb,staycations, Holiday homes &  houses for rent in Kenya!',
        'meta_description': f'Find properties in {display_location_name}. Browse verified listings with photos, amenities, and booking details.' if selected_location != 'all' else 'Find the best properties in Kenya. Browse verified listings for rent, sale, and shortlet.',
    }

    context = prepare_listing_context(request, queryset, context_extra)
    return render(request, 'listings/listings.html', context)


def listings_by_property_type(request, property_type_slug):
    """
    Display listings filtered by property type
    URL example: /property-type/rent_studio/
    Uses listings.html template
    """
    # Get property type mappings
    PROPERTY_TYPE_SLUGS = get_property_type_slug_mappings()
    all_property_types = dict(Listing.PROPERTY_TYPES)

    # Get the property type code from slug
    property_code = PROPERTY_TYPE_SLUGS.get(property_type_slug)

    if not property_code:
        # Handle invalid property type slug
        messages.error(request, 'Invalid property type')
        return redirect('home')  # Changed from 'listing_list' to 'home'

    # Get property display name for template
    property_display_name = all_property_types.get(property_code, property_code.replace('_', ' ').title())

    # Get current location from query params if any
    selected_location = request.GET.get('location', 'all')

    # Get location name for display if location is selected
    location_name = ''
    if selected_location and selected_location != 'all':
        location_dict = dict(Listing.LOCATIONS)
        location_name = location_dict.get(selected_location, selected_location.title())

    # Get location slug for current location (for template)
    LOCATION_SLUGS = get_location_slug_mappings()
    current_location_slug = None
    if selected_location and selected_location != 'all':
        for slug, code in LOCATION_SLUGS.items():
            if code == selected_location:
                current_location_slug = slug
                break

    # Get filtered listings
    queryset = get_filtered_listings(request, property_type=property_code)

    # Prepare context
    context_extra = {
        'property_code': property_code,
        'property_name': property_display_name,
        'property_type_slug': property_type_slug,
        'selected_location': selected_location,
        'selected_listing_type': request.GET.get('listing_type', 'all'),
        'location_name': location_name,
        'current_location_slug': current_location_slug,
        'page_type': 'property_type',
        'is_property_type_page': True,
        'page_title': f'{property_display_name} | Bnb.co.ke',
        'meta_description': f'Find the best {property_display_name} properties in Kenya. Browse listings for bnb,staycations, rent, and shortlet.',
    }

    context = prepare_listing_context(request, queryset, context_extra)
    return render(request, 'listings/listings.html', context)

def all_property_types(request):
    """
    Display all property types with counts (category view)
    Uses a separate template for the category listing
    """
    # Get all property types
    property_types = []

    for code, display_name in Listing.PROPERTY_TYPES:
        # Count active listings for this property type
        count = Listing.objects.filter(
            is_approved=True,
            property_type=code
        ).count()

        # Determine category (residential, commercial, land)
        if code.startswith('rent_') or code.startswith('buy_'):
            category = 'Residential'
            icon = 'fa-home'
        elif code.startswith('commercial') or 'office' in code or 'coworking' in code:
            category = 'Commercial'
            icon = 'fa-building'
        elif 'land' in code:
            category = 'Land'
            icon = 'fa-map'
        else:
            category = 'Other'
            icon = 'fa-tag'

        property_types.append({
            'code': code,
            'name': display_name,
            'slug': code.replace('_', '-'),
            'count': count,
            'category': category,
            'icon': icon,
        })

    # Group by category
    residential = [p for p in property_types if p['category'] == 'Residential']
    commercial = [p for p in property_types if p['category'] == 'Commercial']
    land = [p for p in property_types if p['category'] == 'Land']
    other = [p for p in property_types if p['category'] == 'Other']

    context = {
        'residential_types': residential,
        'commercial_types': commercial,
        'land_types': land,
        'other_types': other,
        'page_title': 'All Property Types | Condo.co.ke',
        'meta_description': 'Browse all property types in Kenya including residential, commercial, and land.',
    }
    return render(request, 'listings/all_property_types.html', context)


# ============================================================================
# LISTING MANAGEMENT VIEWS (Unchanged)
# ============================================================================

@login_required
def submit_listing(request):
    """
    Submit new listing page - Allow authenticated users to submit new listings
    """
    if request.method == 'POST':
        form = ListingSubmissionForm(request.POST, request.FILES, user=request.user)

        # Debug: Print form errors if any
        if not form.is_valid():
            print("Form errors:", form.errors.as_json())
            print("Form non-field errors:", form.non_field_errors())

            # Add detailed error messages for the user
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f"Error: {error}")
                    else:
                        field_label = form.fields[field].label if field in form.fields else field
                        messages.error(request, f"{field_label}: {error}")

            context = {
                'form': form,
                'title': 'Submit New Listing - Bnb.co.ke',
                'featured_price': 1000.00,
            }
            return render(request, 'listings/create_listing.html', context)

        try:
            listing = form.save(commit=False)
            listing_type = form.cleaned_data.get('listing_type', 'free')

            # Set listing type and featured status
            listing.listing_type = listing_type
            listing.is_featured = (listing_type == 'featured')

            # For featured listings, set the payment amount
            if listing_type == 'featured':
                listing.featured_payment_amount = 1000.00

            # Ensure required fields are set
            if not listing.host_name and request.user:
                full_name = f"{request.user.first_name} {request.user.last_name}".strip()
                listing.host_name = full_name if full_name else request.user.username

            if not listing.host_email and request.user:
                listing.host_email = request.user.email

            # Save the listing
            listing.save()

            # Save many-to-many and file fields
            form.save_m2m()

            # Different success messages based on listing type
            if listing_type == 'featured':
                messages.success(request,
                                 f'🎉 Your FEATURED property listing has been submitted successfully! '
                                 f'Please pay KES 1,000 to activate your featured listing. '
                                 f'Once payment is confirmed, your listing will appear at the TOP of search results '
                                 f'and will be approved within 2 hours.'
                                 )
            else:
                messages.success(request,
                                 '🎉 Your FREE property listing has been submitted successfully! '
                                 'It will be reviewed by our team and approved within 24 hours. '
                                 'You will be notified once it\'s live.'
                                 )

            return redirect('my_bnb_listings')  # Redirect to user's listings page

        except Exception as e:
            # Catch any unexpected errors
            messages.error(request, f'An error occurred while saving: {str(e)}')
            import traceback
            traceback.print_exc()  # This will print the full error to your console

            context = {
                'form': form,
                'title': 'Submit New Listing - Condo.co.ke',
                'featured_price': 1000.00,
            }
            return render(request, 'listings/create_listing.html', context)

    else:
        form = ListingSubmissionForm(user=request.user)

    context = {
        'form': form,
        'title': 'Submit New Listing - Condo.co.ke',
        'featured_price': 1000.00,
    }
    return render(request, 'listings/create_listing.html', context)


def book_via_whatsapp(request):
    """
    Simple WhatsApp booking page - Just a big WhatsApp button
    """
    context = {
        'page_title': 'Book via WhatsApp - Instant Booking | Bnb.co.ke',
        'meta_description': 'Book your property directly on WhatsApp. Chat with hosts instantly, get quick responses.',
        'whatsapp_number': '+254798246467',  # Your business WhatsApp number
    }
    return render(request, 'listings/book_via_whatsapp.html', context)


def booking_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, listing=listing, user=request.user if request.user.is_authenticated else None)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing

            # REMOVED: No more date calculations
            # booking.total_price is no longer needed as it's removed from model

            booking.save()

            # Updated success message for inquiry
            messages.success(
                request,
                f"🎉 Your inquiry has been sent successfully! "
                f"Your inquiry reference is {booking.inquiry_ref}. "
                f"The host will contact you shortly on {booking.guest_phone} or {booking.guest_email}."
            )

            return redirect('listing_detail', slug=listing.slug)  # Redirect back to listing page
    else:
        form = BookingForm(initial={'listing_id': listing.id}, listing=listing,
                           user=request.user if request.user.is_authenticated else None)

    context = {
        'form': form,
        'listing': listing,
        'page_title': f' Book{listing.title} | Bnb.co.ke',
    }
    return render(request, 'listings/booking_form.html', context)

def booking_confirmation(request, booking_id):
    """
    Display booking confirmation page
    """
    booking = get_object_or_404(Booking, id=booking_id)
    listing = booking.listing

    context = {
        'booking': booking,
        'listing': listing,
        'booking_ref': f"BK{booking.id:06d}",
        'check_in_formatted': booking.check_in.strftime('%B %d, %Y'),
        'check_out_formatted': booking.check_out.strftime('%B %d, %Y'),
        'total_price_formatted': f"{booking.total_price:,.2f}",
        'number_of_nights': (booking.check_out - booking.check_in).days,
        'page_title': f'Booking Confirmation - BK{booking.id:06d} | Bnb.co.ke',
    }
    return render(request, 'booking_confirmation.html', context)


@login_required
def my_listings(request):
    """
    Display user's listings
    """
    listings = Listing.objects.filter(user=request.user).order_by('-created_at')

    # Statistics
    active_listings = listings.filter(is_approved=True)
    featured_listings = listings.filter(listing_type='featured')

    context = {
        'listings': listings,
        'active_listings': active_listings,
        'featured_listings': featured_listings,
        'pending_bookings': 0,  # You can add this later
        'title': 'My Listings | Bnb.co.ke',
        'page_title': 'My Listings'
    }
    return render(request, 'listings/my_listings.html', context)


@login_required
def edit_listing(request, listing_id):
    """Edit existing listing - only accessible by listing owner"""
    listing = get_object_or_404(Listing, id=listing_id)

    # Check if user owns the listing
    if listing.user != request.user:
        messages.error(request, 'You do not have permission to edit this listing.')
        return redirect('my_bnb_listings')

    if request.method == 'POST':
        form = ListingSubmissionForm(
            request.POST,
            request.FILES,
            instance=listing,
            user=request.user
        )
        if form.is_valid():
            # Handle image deletions before saving
            if request.POST.get('delete_main_image') == 'true':
                listing.main_image.delete(save=False)
                listing.main_image = None

            if request.POST.get('delete_image_2') == 'true':
                if listing.image_2:
                    listing.image_2.delete(save=False)
                listing.image_2 = None

            if request.POST.get('delete_image_3') == 'true':
                if listing.image_3:
                    listing.image_3.delete(save=False)
                listing.image_3 = None

            if request.POST.get('delete_image_4') == 'true':
                if listing.image_4:
                    listing.image_4.delete(save=False)
                listing.image_4 = None

            if request.POST.get('delete_image_5') == 'true':
                if listing.image_5:
                    listing.image_5.delete(save=False)
                listing.image_5 = None

            if request.POST.get('delete_image_6') == 'true':
                if listing.image_6:
                    listing.image_6.delete(save=False)
                listing.image_6 = None

            if request.POST.get('delete_image_7') == 'true':
                if listing.image_7:
                    listing.image_7.delete(save=False)
                listing.image_7 = None

            if request.POST.get('delete_image_8') == 'true':
                if listing.image_8:
                    listing.image_8.delete(save=False)
                listing.image_8 = None

            form.save()
            messages.success(request, 'Listing updated successfully!')
            return redirect('my_bnb_listings')
    else:
        form = ListingSubmissionForm(instance=listing, user=request.user)

    context = {
        'form': form,
        'listing': listing,
        'title': f'Edit {listing.title} | Bnb.co.ke',
        'page_title': 'Edit Listing'
    }
    return render(request, 'listings/edit_listing.html', context)


@login_required
def delete_listing(request, listing_id):
    """Delete listing - only accessible by listing owner"""
    listing = get_object_or_404(Listing, id=listing_id)

    # Check if user owns the listing
    if listing.user != request.user:
        messages.error(request, 'You do not have permission to delete this listing.')
        return redirect('my_bnb_listings')

    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('my_bnb_listings')

    context = {
        'listing': listing,
        'title': f'Delete {listing.title} - Bnb.co.ke',
        'page_title': 'Delete Listing'
    }
    return render(request, 'listings/delete_listing.html', context)


def listing_detail(request, slug):
    """
    Display individual listing detail page
    """
    listing = get_object_or_404(Listing, slug=slug, is_approved=True)

    # Check if user is the owner
    is_owner = request.user.is_authenticated and listing.user == request.user

    context = {
        'listing': listing,
        'is_owner': is_owner,
        'page_title': f' {listing.title} | Bnb.co.ke',
        'meta_description': f'Book {listing.title} in {listing.get_location_display()}. {listing.guests} guests, {listing.bedrooms} bedrooms, KES {listing.price_per_night}/night.',
    }
    return render(request, 'listings/listing_detail.html', context)