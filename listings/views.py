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

# Set up logger
logger = logging.getLogger(__name__)


def listing_list(request, location_slug=None):
    """
    Home page - Display all approved listings or location-specific listings
    """
    # Generate a random seed based on session or current timestamp
    random_seed = request.session.get('random_seed', random.randint(1, 1000000))
    request.session['random_seed'] = random_seed + 1

    # Start with all approved listings
    listings = Listing.objects.filter(is_approved=True)

    # Get all location choices from the model
    all_location_choices = Listing.LOCATIONS
    location_choices_dict = dict(all_location_choices)

    # Dynamically create LOCATION_SLUGS from model LOCATIONS
    LOCATION_SLUGS = {}
    for location_code, location_display_name in all_location_choices:
        # Create slug from location code
        slug = location_code.lower()
        LOCATION_SLUGS[slug] = location_code

    # Get selected location from URL slug or query parameter
    if location_slug:
        selected_location = LOCATION_SLUGS.get(location_slug)
        location_specific = True
    else:
        selected_location = request.GET.get('location', 'all')
        location_specific = False

    # Apply location filter if not 'all'
    if selected_location and selected_location != 'all':
        listings = listings.filter(location=selected_location)

    # Get location name for display
    display_location_name = 'All Locations'
    if selected_location != 'all':
        display_location_name = location_choices_dict.get(selected_location, selected_location.title())

    # Get location slug for current location (for template)
    current_location_slug = None
    if selected_location != 'all':
        # Find the slug for the current location
        for slug, code in LOCATION_SLUGS.items():
            if code == selected_location:
                current_location_slug = slug
                break

    # Other filters
    property_type = request.GET.get('property_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    listing_type = request.GET.get('listing_type', 'all')  # New filter for listing type

    if property_type:
        listings = listings.filter(property_type=property_type)
    if min_price:
        listings = listings.filter(price_per_night__gte=min_price)
    if max_price:
        listings = listings.filter(price_per_night__lte=max_price)
    if listing_type and listing_type != 'all':
        listings = listings.filter(listing_type=listing_type)

    # Get all listings as a list for randomization
    all_listings = list(listings)

    # Separate featured and non-featured listings (featured = listing_type='featured')
    featured_listings = [listing for listing in all_listings if listing.listing_type == 'featured']
    non_featured_listings = [listing for listing in all_listings if listing.listing_type != 'featured']

    # Shuffle both lists separately with the current random seed
    random.seed(random_seed)
    random.shuffle(featured_listings)
    random.shuffle(non_featured_listings)

    # Combine: featured first, then non-featured
    all_listings_shuffled = featured_listings + non_featured_listings

    # Convert back to queryset-like structure for pagination
    class ListPaginator(Paginator):
        def __init__(self, object_list, per_page, **kwargs):
            super().__init__(object_list, per_page, **kwargs)

    # Pagination
    paginator = ListPaginator(all_listings_shuffled, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Create location data with slugs for template
    locations_with_slugs = []
    for location_code, loc_display_name in all_location_choices:
        # Create slug from location code
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

    # Get total count for display
    total_listings = len(all_listings_shuffled)

    # Count featured listings
    featured_count = len(featured_listings)
    free_count = len(non_featured_listings)

    # Get featured listings for slider (only featured listing_type)
    featured_listings_queryset = Listing.objects.filter(
        is_approved=True,
        listing_type='featured'  # Changed from is_featured to listing_type
    )

    if selected_location and selected_location != 'all':
        featured_listings_queryset = featured_listings_queryset.filter(location=selected_location)

    if property_type:
        featured_listings_queryset = featured_listings_queryset.filter(property_type=property_type)
    if min_price:
        featured_listings_queryset = featured_listings_queryset.filter(price_per_night__gte=min_price)
    if max_price:
        featured_listings_queryset = featured_listings_queryset.filter(price_per_night__lte=max_price)

    # Get all featured listings for slider as a list
    all_featured_for_slider = list(featured_listings_queryset)

    # Shuffle featured listings for slider with same random seed
    random.seed(random_seed)
    random.shuffle(all_featured_for_slider)

    # Get up to 3 featured listings for the slider
    featured_slider_listings = all_featured_for_slider[:3]

    # If no featured listings, fallback to first 3 regular listings
    if not featured_slider_listings:
        # Shuffle regular listings for fallback
        regular_listings = list(Listing.objects.filter(
            is_approved=True,
            listing_type='free'  # Free listings
        ))
        random.seed(random_seed)
        random.shuffle(regular_listings)
        featured_slider_listings = regular_listings[:3]

    context = {
        'listings': page_obj,
        'page_obj': page_obj,
        'all_locations': locations_with_slugs,
        'property_types': property_types,
        'listing_types': listing_types,
        'selected_location': selected_location,
        'selected_listing_type': listing_type,
        'location_name': display_location_name,
        'current_location_slug': current_location_slug,
        'location_specific': location_specific,
        'total_listings': total_listings,
        'featured_count': featured_count,
        'free_count': free_count,
        'featured_listings': featured_slider_listings,
        'current_filters': {
            'location': selected_location,
            'property_type': property_type,
            'listing_type': listing_type,
            'min_price': min_price,
            'max_price': max_price,
        },
        'featured_price': 1000.00,  # Added featured price
        'page_title': f'BnB in {display_location_name}' if selected_location != 'all' else 'BnB | staycations in kenya',
        'meta_description': f' Book BnB in {display_location_name}. Find verified properties with photos, amenities, and booking details.',
    }
    return render(request, 'BnB.html', context)


def submit_listing(request):
    """
    Submit new listing page - Allow BnB owners to submit new listings
    """
    if request.method == 'POST':
        form = ListingSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing_type = form.cleaned_data.get('listing_type', 'free')

            # Set listing type and featured status
            listing.listing_type = listing_type
            listing.is_featured = (listing_type == 'featured')

            # For featured listings, set the payment amount
            if listing_type == 'featured':
                listing.featured_payment_amount = 1000.00

            # Save the listing
            listing.save()

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

            return redirect('submit_listing')  # Redirect back to the same form page
    else:
        form = ListingSubmissionForm()

    context = {
        'form': form,
        'title': 'Submit New Listing',
        'featured_price': 1000.00,
    }
    return render(request, 'ADVERTISEBNB.html', context)


def book_via_whatsapp(request):
    """
    Simple WhatsApp booking page - Just a big WhatsApp button
    """
    context = {
        'page_title': 'Book BnB via WhatsApp - Instant Booking',
        'meta_description': 'Book your vacation rental directly on WhatsApp. Chat with hosts instantly, get quick responses.',
        'whatsapp_number': '+254707341748',  # Your business WhatsApp number
    }
    return render(request, 'BOOKVIAWHATSAPP.html', context)


def send_booking_confirmation_email(booking):
    """Send booking confirmation email to guest"""

    try:
        # Calculate number of nights
        number_of_nights = (booking.check_out - booking.check_in).days

        # Email context data
        context = {
            'booking': booking,
            'listing': booking.listing,
            'booking_ref': f"BK{booking.id:06d}",
            'check_in': booking.check_in.strftime('%B %d, %Y'),
            'check_out': booking.check_out.strftime('%B %d, %Y'),
            'total_price': f"{booking.total_price:,.2f}",
            'number_of_nights': number_of_nights,
            'price_per_night': f"{booking.listing.price_per_night:,.2f}",
        }

        # Render HTML email template
        html_message = render_to_string('emails/BOOKING_CONFIRMATION.html', context)
        plain_message = strip_tags(html_message)  # Create plain text version

        # Email subject
        subject = f"Booking Confirmation - {booking.listing.title} (Ref: BK{booking.id:06d})"

        # Sender and recipient
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'booking.bnb.co.ke@gmail.com')
        recipient_list = [booking.guest_email]

        # Send email to guest
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(f"Booking confirmation email sent to {booking.guest_email} for booking BK{booking.id:06d}")

        # Optionally send a copy to admin
        admin_email = getattr(settings, 'ADMIN_EMAIL', None)
        if admin_email:
            admin_subject = f"New Booking Notification - {booking.listing.title}"
            admin_message = (
                f"New booking received!\n\n"
                f"Guest: {booking.guest_name}\n"
                f"Email: {booking.guest_email}\n"
                f"Phone: {booking.guest_phone}\n"
                f"Property: {booking.listing.title}\n"
                f"Booking Ref: BK{booking.id:06d}\n"
                f"Dates: {booking.check_in.strftime('%Y-%m-%d')} to {booking.check_out.strftime('%Y-%m-%d')}\n"
                f"Nights: {number_of_nights}\n"
                f"Guests: {booking.number_of_guests}\n"
                f"Total: KES {booking.total_price:,.2f}\n"
                f"Price per night: KES {booking.listing.price_per_night:,.2f}"
            )

            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=from_email,
                recipient_list=[admin_email],
                fail_silently=True,
            )

            logger.info(f"Admin notification sent to {admin_email} for booking BK{booking.id:06d}")

    except Exception as e:
        logger.error(f"Failed to send booking email for booking BK{booking.id:06d}: {e}")
        # Don't raise the exception to avoid breaking the booking process


def booking_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, listing=listing)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing

            # Calculate total price
            number_of_nights = (booking.check_out - booking.check_in).days
            booking.total_price = number_of_nights * listing.price_per_night

            booking.save()

            # Send confirmation email
            send_booking_confirmation_email(booking)

            # Store booking ID in session for PDF download
            request.session['last_booking_id'] = booking.id

            # Clear the form for new submission
            form = BookingForm(initial={'listing_id': listing.id}, listing=listing)

            # Add success message using Django messages
            messages.success(
                request,
                f"🎉 Booking request sent successfully! "
                f"Your booking reference is BK{booking.id:06d}. "
                f"Please allow us few minutes to confirm your booking! "
                f"You will receive a text or call on  {booking.guest_phone} & a  confirmation email on {booking.guest_email}."
            )

            context = {
                'form': form,
                'listing': listing,
                'page_title': f'Book {listing.title}',
                'booking_id': booking.id,  # Pass booking_id to template
                'booking_details': {
                    'guest_name': booking.guest_name,
                    'guest_email': booking.guest_email,
                    'guest_phone': booking.guest_phone,
                    'check_in': booking.check_in.strftime('%B %d, %Y'),
                    'check_out': booking.check_out.strftime('%B %d, %Y'),
                    'number_of_guests': booking.number_of_guests,
                    'total_price': f"{booking.total_price:,.2f}",
                    'booking_ref': f"BK{booking.id:06d}",
                    'number_of_nights': number_of_nights,
                }
            }
            return render(request, 'BOOKINGFORM.html', context)
    else:
        form = BookingForm(initial={'listing_id': listing.id}, listing=listing)

    context = {
        'form': form,
        'listing': listing,
        'page_title': f'Book {listing.title}',
    }
    return render(request, 'BOOKINGFORM.html', context)


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
        'page_title': f'Booking Confirmation - BK{booking.id:06d}',
    }

    return render(request, 'BOOKING_CONFIRMATION.html', context)