# auth/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone

from .forms import (
    UserRegisterForm, UserLoginForm, UserUpdateForm,
    ProfileUpdateForm, PasswordResetForm, PasswordResetConfirmForm
)
from .models import UserProfile
from listings.models import Listing, Booking


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Log the user in
            login(request, user)

            messages.success(
                request,
                f'🎉 Account created successfully! Welcome {username}.'
            )

            # Send welcome email with HTML template
            try:
                subject = 'Welcome to BnB Ke!'

                # Create welcome email context
                welcome_context = {
                    'user': user,
                    'username': username,
                    'site_name': 'BnB Ke',
                    'login_url': request.build_absolute_uri(reverse('login')),
                    'profile_url': request.build_absolute_uri(reverse('profile')),
                    'listings_url': request.build_absolute_uri(reverse('advertise_bnb')),
                }

                # Render HTML email
                html_message = render_to_string('auth/welcome_email.html', welcome_context)

                # Plain text version
                plain_message = f"""Welcome to BnB Ke, {username}!

Thank you for registering with BnB Ke. You can now:

• Create and manage property listings
• Book properties for your staycations
• Manage your profile and bookings
• Connect with other hosts and guests

Get started by creating your first listing: {welcome_context['listings_url']}

If you have any questions, feel free to contact our support team.

Best regards,
The BnB Ke Team"""

                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    html_message=html_message,
                    fail_silently=True,
                )
            except Exception as e:
                # Log the error but don't break registration
                print(f"Welcome email failed: {e}")

            # Redirect to profile or next parameter
            next_url = request.GET.get('next', 'profile')
            return redirect(next_url)
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'Register - BnB Ke',
        'page_title': 'Create Account'
    }
    return render(request, 'auth/register.html', context)


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Handle remember me
            remember_me = request.POST.get('remember_me')
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when browser closes

            messages.success(request, f'Welcome back, {user.username}!')

            # Redirect to next parameter or profile
            next_url = request.GET.get('next', 'profile')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
        'title': 'Login - BnB Ke',
        'page_title': 'Sign In'
    }
    return render(request, 'auth/login.html', context)


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """User profile view"""
    user = request.user

    if request.method == 'POST':
        # Handle profile picture upload separately
        if 'profile_picture' in request.FILES:
            p_form = ProfileUpdateForm(
                request.POST,
                request.FILES,
                instance=user.profile
            )
            if p_form.is_valid():
                p_form.save()
                messages.success(request, 'Profile picture updated!')
                return redirect('profile')

        # Handle form type detection
        form_type = request.POST.get('form_type')

        if form_type == 'profile_update':
            u_form = UserUpdateForm(request.POST, instance=user)
            p_form = ProfileUpdateForm(
                request.POST,
                request.FILES,
                instance=user.profile
            )

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile')
        else:
            # Handle profile picture upload from hidden form
            p_form = ProfileUpdateForm(
                request.POST,
                request.FILES,
                instance=user.profile
            )
            if p_form.is_valid():
                p_form.save()
                messages.success(request, 'Profile picture updated!')
                return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    # Get user's listings with statistics
    user_listings = Listing.objects.filter(user=user).order_by('-created_at')
    approved_listings_count = user_listings.filter(is_approved=True).count()
    featured_listings_count = user_listings.filter(listing_type='featured').count()

    # Get booking statistics
    bookings_count = Booking.objects.filter(user=user).count()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user,
        'user_listings': user_listings,
        'bookings_count': bookings_count,
        'approved_listings_count': approved_listings_count,
        'featured_listings_count': featured_listings_count,
        'title': 'Profile - BnB Ke',
        'page_title': 'My Profile'
    }
    return render(request, 'auth/profile.html', context)


@login_required
def delete_account(request):
    """Handle account deletion request"""
    if request.method == 'POST':
        user = request.user
        email = user.email

        # Send confirmation email before deletion
        try:
            subject = 'Account Deletion Request - BnB Ke'
            message = f"""Hello {user.get_full_name() or user.username},

Your account deletion request has been received. 
Your account will be permanently deleted in 7 days.

If you did not request this, please contact our support team immediately at {settings.ADMIN_EMAIL}.

Best regards,
The BnB Ke Team"""

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass

        # Log the user out
        logout(request)

        # Schedule account deletion (in production, use Celery or similar)
        # For now, just show a message
        messages.info(request,
                      'Your account deletion request has been received. You will receive a confirmation email.')
        return redirect('home')

    return redirect('profile')



def my_listings(request):
    """Display user's listings (moved from auth app for better organization)"""
    if not request.user.is_authenticated:
        return redirect('login')

    listings = Listing.objects.filter(user=request.user).order_by('-created_at')

    # Statistics
    active_listings = listings.filter(is_approved=True)
    featured_listings = listings.filter(listing_type='featured')

    context = {
        'listings': listings,
        'active_listings': active_listings,
        'featured_listings': featured_listings,
        'pending_bookings': 0,  # You can add this later
        'title': 'My Listings - BnB Ke',
        'page_title': 'My Listings'
    }
    return render(request, 'auth/profile.html', context)