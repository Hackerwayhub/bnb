from django import forms
from .models import Booking, Listing
import re
from datetime import date
from django.contrib.auth.models import User


class ListingSubmissionForm(forms.ModelForm):
    # Add listing_type field as a radio select
    listing_type = forms.ChoiceField(
        choices=Listing.LISTING_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='free',
        label="Choose Listing Type",
        help_text="Select how you want to list your property"
    )

    class Meta:
        model = Listing
        fields = [
            'title', 'property_type', 'transaction_type', 'location', 'specific_location', 'address',
            'host_phone', 'host_whatsapp',
            # Property details
            'guests', 'bedrooms', 'beds', 'bathrooms', 'en_suites', 'living_rooms', 'kitchens',
            # Size
            'land_size', 'land_size_unit', 'floor_area',
            # Property condition
            'year_built', 'condition', 'furnishing',
            # Parking
            'parking_spots', 'covered_parking', 'visitor_parking',
            # Floors
            'total_floors', 'floor_number',
            # Additional rooms
            'servant_quarters', 'store_rooms',
            # AMENITIES - Basic
            'wifi', 'parking', 'kitchen',
            # Fitness & Wellness
            'gym', 'pool', 'spa', 'sauna', 'steam_room',
            # Climate Control
            'ac', 'heating', 'ceiling_fans', 'fireplace',
            # Entertainment
            'tv', 'sound_system', 'home_theater',
            # Outdoor
            'balcony', 'terrace', 'garden', 'roof_terrace', 'bbq_area', 'outdoor_shower',
            # Security
            'cctv', 'security_guards', 'electric_fence', 'secure_compound', 'alarm_system',
            # Utilities
            'generator', 'solar_panels', 'water_tank', 'borehole', 'backup_water', 'internet_fiber',
            # Building Amenities
            'elevator', 'wheelchair_accessible', 'reception', 'lobby', 'concierge', 'laundry_room', 'play_area',
            'pet_friendly',
            # Staff
            'house_staff', 'askari', 'caretaker',
            # Pricing
            'price', 'service_charge', 'deposit_required', 'utilities_included', 'title_deed', 'loan_available',
            # Availability
            'available_from', 'available_to', 'minimum_stay', 'maximum_stay',
            # Media
            'main_image', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6', 'image_7', 'image_8',
            'virtual_tour_url', 'youtube_video_id',
            # Map
            'latitude', 'longitude',
            # Extra
            'whatsapp_group_link',
            'listing_type'
        ]
        widgets = {
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'specific_location': forms.TextInput(
                attrs={'placeholder': 'e.g., "Near ABC Mall, Spring Valley Estate", etc.'}),
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Full physical address (optional)'}),
            'host_phone': forms.TextInput(attrs={'placeholder': '+254712345678'}),
            'host_whatsapp': forms.TextInput(attrs={'placeholder': '+254712345678'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Beautiful 3-Bedroom Apartment with City View'
            }),
            # Property details
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'beds': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'en_suites': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'living_rooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'kitchens': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),

            # Size
            'land_size': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g., 0.25'}),
            'land_size_unit': forms.Select(attrs={'class': 'form-control'}),
            'floor_area': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g., 150'}),

            # Property condition
            'year_built': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2020'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'furnishing': forms.Select(attrs={'class': 'form-control'}),

            # Parking
            'parking_spots': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),

            # Floors
            'total_floors': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),

            # Checkboxes for all amenities (styled)
            'wifi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'kitchen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gym': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'spa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sauna': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'steam_room': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ac': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'heating': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ceiling_fans': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fireplace': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tv': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sound_system': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'home_theater': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'balcony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'terrace': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'garden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'roof_terrace': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bbq_area': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'outdoor_shower': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cctv': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'security_guards': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'electric_fence': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'secure_compound': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alarm_system': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'generator': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'solar_panels': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'water_tank': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'borehole': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'backup_water': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'internet_fiber': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'elevator': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wheelchair_accessible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reception': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lobby': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'concierge': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'laundry_room': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'play_area': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pet_friendly': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'house_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'askari': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'caretaker': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'servant_quarters': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'store_rooms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'covered_parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'visitor_parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'utilities_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'title_deed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'loan_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # Pricing
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 15000'}),
            'service_charge': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3000'}),
            'deposit_required': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 15000'}),

            # Availability
            'available_from': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'available_to': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'minimum_stay': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
            'maximum_stay': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 365}),

            # Media
            'main_image': forms.FileInput(attrs={'class': 'form-control', 'required': True}),
            'image_2': forms.FileInput(attrs={'class': 'form-control'}),
            'image_3': forms.FileInput(attrs={'class': 'form-control'}),
            'image_4': forms.FileInput(attrs={'class': 'form-control'}),
            'image_5': forms.FileInput(attrs={'class': 'form-control'}),
            'image_6': forms.FileInput(attrs={'class': 'form-control'}),
            'image_7': forms.FileInput(attrs={'class': 'form-control'}),
            'image_8': forms.FileInput(attrs={'class': 'form-control'}),

            # Virtual tour
            'virtual_tour_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'youtube_video_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., dQw4w9WgXcQ'}),

            # Map
            'latitude': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.000001', 'placeholder': '-1.2921'}),
            'longitude': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.000001', 'placeholder': '36.8219'}),

            # Extra
            'whatsapp_group_link': forms.URLInput(
                attrs={'class': 'form-control', 'placeholder': 'https://chat.whatsapp.com/...'}),
            'listing_type': forms.RadioSelect(attrs={'class': 'listing-type-radio'}),
        }
        help_texts = {
            'host_whatsapp': 'This number will be used by guests to contact you via WhatsApp',
            'host_phone': 'This number will be used by guests to call you',
            'specific_location': 'Provide specific details like estate name, landmarks, etc.',
            'address': 'Full physical address (optional but recommended)',
            'price': 'Enter the price in Kenyan Shillings (KES). For rent: monthly, for sale: total price',
            'land_size': 'Size of land (if applicable)',
            'floor_area': 'Built-up area / floor area in square meters',
            'virtual_tour_url': 'Link to Matterport, 3D tour, or video walkthrough',
            'available_from': 'Date from which property is available',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Mark required fields
        required_fields = [
            'title', 'property_type', 'transaction_type', 'location', 'specific_location',
            'host_phone', 'host_whatsapp', 'guests', 'bedrooms', 'beds', 'bathrooms', 'price',
            'main_image'
        ]

        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                if not self.fields[field_name].label:
                    self.fields[field_name].label = field_name.replace('_', ' ').title()
                self.fields[field_name].widget.attrs['required'] = True

        # Pre-fill contact info from user profile
        if self.user and hasattr(self.user, 'profile'):
            profile = self.user.profile
            if profile.phone:
                self.fields['host_phone'].initial = profile.phone
            if profile.whatsapp:
                self.fields['host_whatsapp'].initial = profile.whatsapp

        # Add CSS classes to all form fields
        for field_name, field in self.fields.items():
            if field_name not in ['listing_type'] and not isinstance(field.widget,
                                                                     forms.CheckboxInput) and not isinstance(
                field.widget, forms.RadioSelect):
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'

        # Set initial values
        self.fields['guests'].initial = 2
        self.fields['bedrooms'].initial = 1
        self.fields['beds'].initial = 1
        self.fields['bathrooms'].initial = 1
        self.fields['living_rooms'].initial = 1
        self.fields['kitchens'].initial = 1
        self.fields['minimum_stay'].initial = 1
        self.fields['maximum_stay'].initial = 365

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set user and auto-fill host info
        if self.user:
            instance.user = self.user
            instance.host_email = self.user.email

            # Set host_name from user profile
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
            instance.host_name = full_name if full_name else self.user.username

        # Set price_per_night or price_per_month based on transaction_type
        if instance.transaction_type == 'shortlet' and instance.price:
            instance.price_per_night = instance.price
        elif instance.transaction_type == 'rent' and instance.price:
            instance.price_per_month = instance.price

        if commit:
            instance.save()
            # Save many-to-many relationships
            self.save_m2m()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        price = cleaned_data.get('price')

        # Validate price based on transaction type
        if transaction_type and price:
            if transaction_type == 'shortlet' and price < 500:
                self.add_error('price', 'Shortlet price per night should be at least KES 500')
            elif transaction_type == 'rent' and price < 2000:
                self.add_error('price', 'Monthly rent should be at least KES 2,000')
            elif transaction_type == 'sale' and price < 500000:
                self.add_error('price', 'Sale price should be at least KES 500,000')

        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than 0")
        return price

    def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        if guests is not None and guests <= 0:
            raise forms.ValidationError("Number of guests must be greater than 0")
        return guests

    def clean_bedrooms(self):
        bedrooms = self.cleaned_data.get('bedrooms')
        if bedrooms is not None and bedrooms < 0:
            raise forms.ValidationError("Number of bedrooms cannot be negative")
        return bedrooms

    def clean_beds(self):
        beds = self.cleaned_data.get('beds')
        if beds is not None and beds <= 0:
            raise forms.ValidationError("Number of beds must be greater than 0")
        return beds

    def clean_bathrooms(self):
        bathrooms = self.cleaned_data.get('bathrooms')
        if bathrooms is not None and bathrooms < 0:
            raise forms.ValidationError("Number of bathrooms cannot be negative")
        return bathrooms


class BookingForm(forms.ModelForm):
    listing_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'guest_phone', 'message', 'inquiry_type']
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'id': 'guest_name'
            }),
            'guest_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com',
                'id': 'guest_email'
            }),
            'guest_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+2547XXXXXXXX',
                'id': 'guest_phone'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about your inquiry...',
                'id': 'message'
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'inquiry_type'
            }),
        }
        help_texts = {
            'guest_phone': 'Please include country code (e.g., +2547XXXXXXXX)',
        }

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Pre-fill guest info from user profile if authenticated
        if self.user and self.user.is_authenticated:
            self.fields['guest_name'].initial = f"{self.user.first_name} {self.user.last_name}".strip()
            self.fields['guest_email'].initial = self.user.email

            if hasattr(self.user, 'profile') and self.user.profile.phone:
                self.fields['guest_phone'].initial = self.user.profile.phone

        # Set listing_id initial value
        if self.listing:
            self.fields['listing_id'].initial = self.listing.id

        # Make fields required
        self.fields['guest_name'].required = True
        self.fields['guest_email'].required = True
        self.fields['guest_phone'].required = True

        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            if field_name != 'listing_id':
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set listing
        if self.listing:
            instance.listing = self.listing

        # Set user if authenticated
        if self.user and self.user.is_authenticated:
            instance.user = self.user

        if commit:
            instance.save()
        return instance

    def clean_guest_email(self):
        email = self.cleaned_data.get('guest_email')
        if email:
            # Basic email validation
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                raise forms.ValidationError("Please enter a valid email address")
        return email

    def clean_guest_phone(self):
        phone = self.cleaned_data.get('guest_phone')
        if phone:
            # Remove any non-digit characters except +
            cleaned = re.sub(r'[^\d+]', '', phone)

            # Kenyan phone validation
            if cleaned.startswith('+254'):
                if len(cleaned) != 13:  # +2547XXXXXXXX = 13 characters
                    raise forms.ValidationError("Please enter a valid Kenyan phone number (+2547XXXXXXXX)")
            elif cleaned.startswith('0'):
                if len(cleaned) != 10:  # 07XXXXXXXX = 10 digits
                    raise forms.ValidationError("Please enter a valid Kenyan phone number (07XXXXXXXX)")
                # Convert to international format
                cleaned = '+254' + cleaned[1:]
            elif len(cleaned) == 9 and cleaned.isdigit():  # 7XXXXXXXX = 9 digits
                cleaned = '+254' + cleaned
            else:
                raise forms.ValidationError("Please enter a valid phone number (e.g., +2547XXXXXXXX or 07XXXXXXXX)")

            return cleaned
        return phone

    def clean(self):
        cleaned_data = super().clean()

        # Ensure we have at least a message or inquiry_type
        message = cleaned_data.get('message')
        inquiry_type = cleaned_data.get('inquiry_type')

        if not message and not inquiry_type:
            # If both are empty, that's fine - just a basic inquiry
            pass

        return cleaned_data