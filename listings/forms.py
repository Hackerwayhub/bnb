from django import forms
from .models import Booking, Listing
from datetime import date


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
            'title', 'property_type', 'location', 'specific_location',
            'host_name', 'host_phone', 'host_whatsapp',
            'guests', 'bedrooms', 'beds', 'bathrooms',
            'wifi', 'parking', 'kitchen', 'pool', 'ac', 'tv',
            'price_per_night', 'main_image', 'image_2', 'image_3', 'image_4',
            'listing_type'  # Added listing_type
        ]
        widgets = {
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'specific_location': forms.TextInput(attrs={'placeholder': 'e.g., e.g., "Near ABC Mall, 5 minutes from the city center", etc.'}),
            'host_phone': forms.TextInput(attrs={'placeholder': '+254712345678'}),
            'host_whatsapp': forms.TextInput(attrs={'placeholder': '+254712345678'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Beautiful 3-Bedroom Apartment with City View'
            }),
            'host_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'beds': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'image_2': forms.FileInput(attrs={'class': 'form-control'}),
            'image_3': forms.FileInput(attrs={'class': 'form-control'}),
            'image_4': forms.FileInput(attrs={'class': 'form-control'}),
            'wifi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'kitchen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ac': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tv': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'listing_type': forms.RadioSelect(attrs={'class': 'listing-type-radio'}),
        }
        help_texts = {
            'host_whatsapp': 'This number will be used by guests to contact you via WhatsApp',
            'host_phone': 'This number will be used by guests to call you',
            'specific_location': 'Provide specific details like estate name, landmarks, etc.',
            'price_per_night': 'Enter the price per night in Kenyan Shillings (KES)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Admin contact is not in fields, it's automatically set
        self.fields['host_phone'].required = True
        self.fields['host_whatsapp'].required = True

        # Add CSS classes to all form fields
        for field_name, field in self.fields.items():
            if field_name not in ['wifi', 'parking', 'kitchen', 'pool', 'ac', 'tv', 'listing_type']:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'

        # Add specific styling for number fields
        for field_name in ['guests', 'bedrooms', 'beds', 'bathrooms', 'price_per_night']:
            self.fields[field_name].widget.attrs.update({
                'min': '1',
                'step': '1'
            })

        # Add placeholder for price field
        self.fields['price_per_night'].widget.attrs['placeholder'] = 'e.g., 5000'

        # Make main image required
        self.fields['main_image'].required = True

        # Set initial value for listing_type radio buttons
        self.fields['listing_type'].initial = 'free'

    def clean(self):
        cleaned_data = super().clean()
        listing_type = cleaned_data.get('listing_type')

        # Additional validation if needed for featured listings
        if listing_type == 'featured':
            # You can add specific validation for featured listings here
            # For example, ensure certain fields are filled or meet criteria
            pass

        return cleaned_data

    def clean_price_per_night(self):
        price = self.cleaned_data.get('price_per_night')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price per night must be greater than 0")
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
        fields = ['guest_name', 'guest_email', 'guest_phone', 'check_in',
                  'check_out', 'number_of_guests', 'special_requests']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guest_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'guest_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'guest_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+2547XXXXXXXX'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'special_requests': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requirements or questions...'}),
        }
        help_texts = {
            'guest_phone': 'Please include country code (e.g., +2547XXXXXXXX)',
        }

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing', None)
        super().__init__(*args, **kwargs)

        # Set minimum date to today
        today = date.today().isoformat()
        self.fields['check_in'].widget.attrs['min'] = today
        self.fields['check_out'].widget.attrs['min'] = today

        if self.listing:
            self.fields['number_of_guests'].widget.attrs['max'] = self.listing.guests

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        number_of_guests = cleaned_data.get('number_of_guests')

        # Validate dates
        if check_in and check_out:
            if check_in < date.today():
                raise forms.ValidationError("Check-in date cannot be in the past")

            if check_out <= check_in:
                raise forms.ValidationError("Check-out date must be after check-in date")

            # Check if dates overlap with existing bookings
            if self.listing:
                overlapping_bookings = Booking.objects.filter(
                    listing=self.listing,
                    status__in=['confirmed', 'pending'],
                    check_in__lt=check_out,
                    check_out__gt=check_in
                ).exists()

                if overlapping_bookings:
                    raise forms.ValidationError("These dates are not available. Please select different dates.")

        # Validate number of guests
        if number_of_guests and self.listing:
            if number_of_guests > self.listing.guests:
                raise forms.ValidationError(f"This property accommodates maximum {self.listing.guests} guests")

        return cleaned_data