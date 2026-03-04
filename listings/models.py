from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings


class Listing(models.Model):
    # Property Types
    PROPERTY_TYPES = [
        ('studio_staycation', 'Bnb | studio'),
        ('one_bedroom_staycation', 'Bnb | One Bedroom staycation'),
        ('two_bedroom_staycation', 'Bnb | Two Bedroom staycation'),
        ('three_bedroom_staycation', ' Bnb | Three Bedroom staycation'),
        ('Own_compound_staycation', 'Bnb | Own compound/villa staycation'),
        ('beach_house_staycation', 'Bnb| beach house staycation'),
        ('studio', ' Furnished Houses for rent | Studio  '),
        ('one_bedroom', 'Furnished Houses for rent | One Bedroom '),
        ('two_bedroom', 'Furnished Houses for rent | Two Bedroom '),
        ('three_bedroom', 'Furnished Houses for rent | Three Bedroom  '),
        ('Own_compound', 'Furnished Houses for rent | Own compound'),
        ('beach_house', 'Furnished Houses for rent | beach house '),
    ]

    LOCATIONS = [

        ('dubai', 'Dubai'),
        ('usa', 'usa'),
        ('Kenya', 'Kenya'),
        ('westlands', 'Westlands'),
        ('kilimani', 'Kilimani'),
        ('kileleshwa', 'Kileleshwa'),
        ('pangani', 'Pangani'),
        ('parklands', 'Parklands'),
        ('ngara', 'Ngara'),
        ('garden_city', 'Garden City'),
        ('roysambu', 'Roysambu'),
        ('roasters', 'Roasters'),
        ('mirema', 'Mirema'),
        ('Trm_drive', 'Trm drive'),
        ('Lumumba_drive', 'Lumumba drive'),
        ('kitisuru', 'Kitisuru'),
        ('lavington', 'Lavington'),
        ('loresho', 'Loresho'),
        ('zimmerman', 'Zimmerman'),
        ('kahawa_sukari', 'Kahawa Sukari'),
        ('kahawa_wendani', 'Kahawa Wendani'),
        ('kasarani', 'Kasarani'),
        ('bypass', 'Bypass'),
        ('Membley', 'Membley'),
        ('ruiru', 'Ruiru'),
        ('kiambu', 'Kiambu'),
        ('thome', 'Thome'),
        ('kiambu_road', 'Kiambu Road'),
        ('ngong', 'Ngong'),
        ('rongai', 'Rongai'),
        ('gwakairu', 'Gwakairu'),
        ('kimbo', 'Kimbo'),
        ('k_road', 'K Road'),
        ('juja', 'Juja'),
        ('thika', 'Thika'),
        ('kahawa_west', 'Kahawa West'),
        ('kitengela', 'Kitengela'),
        ('watamu', 'Watamu'),
        ('diani', 'Diani'),
        ('embakasi', 'Embakasi'),
        ('fedha', 'Fedha'),
        ('south_b', 'South B'),
        ('south_c', 'South C'),
        ('utawala', 'Utawala'),
        ('mombasa', 'Mombasa'),
        ('eldoret', 'Eldoret'),
        ('nakuru', 'Nakuru'),
        ('naivasha', 'Naivasha'),
        ('homeland', 'Homeland'),
        ('hurlingham', 'Hurlingham'),
        ('kabete', 'Kabete'),
        ('kangemi', 'Kangemi'),
        ('karen', 'Karen'),
        ('kawangware', 'Kawangware'),
        ('milimani', 'Milimani'),
        ('muthaiga', 'Muthaiga'),
        ('mwiki', 'Mwiki'),
        ('nairobi_west', 'Nairobi West'),
        ('ongata_rongai', 'Ongata Rongai'),
        ('ruai', 'Ruai'),
        ('ruaka', 'Ruaka'),
        ('ruaraka', 'Ruaraka'),
        ('runda', 'Runda'),
        ('saika', 'Saika'),
        ('syokimau', 'Syokimau'),
        ('thogoto', 'Thogoto'),
        ('upper_hill', 'Upper Hill'),
        ('uthiru', 'Uthiru'),
        ('athiriver', 'Athiriver'),
        ('kisumu', 'Kisumu'),
        ('machakos', 'Machakos'),
        ('meru_town', 'Meru Town'),
        ('nanyuki', 'Nanyuki'),
        ('nyeri_town', 'Nyeri Town'),
        ('embu_town', 'Embu Town'),
        ('narok_town', 'Narok Town'),
        ('kisii_town', 'Kisii Town'),
        ('voi', 'Voi'),
        ('isiolo_town', 'Isiolo Town'),
        ('bomet', 'Bomet'),
        ('kakamega_town', 'Kakamega Town'),
        ('limuru', 'Limuru'),
        ('malindi', 'Malindi'),
        ('nyahururu', 'Nyahururu'),
        ('migori_town', 'Migori Town'),
        ('kitui_town', 'Kitui Town'),
        ('bungoma_town', 'Bungoma Town'),
        ('kilifi_town', 'Kilifi Town'),
        ('wangige', 'Wangige'),
        ('kericho_town', 'Kericho Town'),
    ]

    LISTING_TYPE_CHOICES = [
        ('free', 'Free Listing'),
        ('featured', 'Featured Listing'),
    ]

    TRANSACTION_TYPE_CHOICES = [
        ('shortlet', 'Bnb / staycation'),
        ('rent', 'For Rent'),
        ('sale', 'For Sale'),
    ]

    PROPERTY_CONDITION_CHOICES = [
        ('new', 'New Construction'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('renovated', 'Recently Renovated'),
        ('under_construction', 'Under Construction'),
    ]

    FURNISHING_CHOICES = [
        ('unfurnished', 'Unfurnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('fully_furnished', 'Fully Furnished'),
    ]

    # Property Details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, default='shortlet')
    location = models.CharField(max_length=100, choices=LOCATIONS)
    specific_location = models.CharField(max_length=200, help_text="Specific area/estate")
    address = models.CharField(max_length=300, blank=True, null=True, help_text="Full address (optional)")

    # Contact Information
    host_name = models.CharField(max_length=100)
    host_email = models.EmailField(max_length=255, blank=True, null=True)

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+254712345678'"
    )

    host_phone = models.CharField(max_length=15, validators=[phone_validator])
    host_whatsapp = models.CharField(max_length=15, validators=[phone_validator])

    # Default admin contact
    admin_contact = models.CharField(
        max_length=15,
        default='+254798246467',
        validators=[phone_validator],
        help_text="Default admin contact number"
    )

    # Listing Type & Pricing
    listing_type = models.CharField(
        max_length=20,
        choices=LISTING_TYPE_CHOICES,
        default='free',
        verbose_name="Listing Type"
    )

    featured_payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000.00,
        verbose_name="Featured Payment Amount"
    )

    # REAL ESTATE SPECIFIC FIELDS
    # Size
    land_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Land size (in acres or sq meters)"
    )
    land_size_unit = models.CharField(
        max_length=20,
        choices=[
            ('sqm', 'Square Meters'),
            ('acres', 'Acres'),
            ('sqft', 'Square Feet'),
        ],
        default='sqm',
        blank=True,
        null=True
    )

    floor_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Floor area / built-up area (in sq meters)"
    )

    # Property Features
    guests = models.PositiveIntegerField(default=1)
    bedrooms = models.PositiveIntegerField(default=1)
    beds = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    en_suites = models.PositiveIntegerField(default=0, blank=True, null=True, help_text="Number of en-suite bathrooms")

    # Additional rooms
    living_rooms = models.PositiveIntegerField(default=1, blank=True, null=True)
    dining_rooms = models.PositiveIntegerField(default=1, blank=True, null=True)
    kitchens = models.PositiveIntegerField(default=1, blank=True, null=True)
    servant_quarters = models.BooleanField(default=False)
    store_rooms = models.BooleanField(default=False)

    # Floors
    total_floors = models.PositiveIntegerField(default=1, blank=True, null=True, help_text="Total floors in building")
    floor_number = models.PositiveIntegerField(default=1, blank=True, null=True,
                                               help_text="Floor number (for apartments)")

    # Property condition
    year_built = models.PositiveIntegerField(blank=True, null=True, help_text="Year property was built")
    condition = models.CharField(max_length=20, choices=PROPERTY_CONDITION_CHOICES, default='good', blank=True,
                                 null=True)
    furnishing = models.CharField(max_length=20, choices=FURNISHING_CHOICES, default='unfurnished', blank=True,
                                  null=True)

    # Parking
    parking_spots = models.PositiveIntegerField(default=0, blank=True, null=True, help_text="Number of parking spots")
    covered_parking = models.BooleanField(default=False)
    visitor_parking = models.BooleanField(default=False)

    # EXPANDED AMENITIES
    # Basic
    wifi = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)

    # Fitness & Wellness
    gym = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    spa = models.BooleanField(default=False)
    sauna = models.BooleanField(default=False)
    steam_room = models.BooleanField(default=False)

    # Climate Control
    ac = models.BooleanField(default=False)
    heating = models.BooleanField(default=False)
    ceiling_fans = models.BooleanField(default=False)
    fireplace = models.BooleanField(default=False)

    # Entertainment
    tv = models.BooleanField(default=False)
    sound_system = models.BooleanField(default=False)
    home_theater = models.BooleanField(default=False)

    # Outdoor
    balcony = models.BooleanField(default=False)
    terrace = models.BooleanField(default=False)
    garden = models.BooleanField(default=False)
    roof_terrace = models.BooleanField(default=False)
    bbq_area = models.BooleanField(default=False)
    outdoor_shower = models.BooleanField(default=False)

    # Security
    cctv = models.BooleanField(default=False)
    security_guards = models.BooleanField(default=False)
    electric_fence = models.BooleanField(default=False)
    secure_compound = models.BooleanField(default=False)
    alarm_system = models.BooleanField(default=False)  # This replaced 'lyft'

    # Utilities
    generator = models.BooleanField(default=False)
    solar_panels = models.BooleanField(default=False)
    water_tank = models.BooleanField(default=False)
    borehole = models.BooleanField(default=False)
    backup_water = models.BooleanField(default=False)
    internet_fiber = models.BooleanField(default=False)

    # Building Amenities
    elevator = models.BooleanField(default=False, help_text="Lift/Elevator")
    wheelchair_accessible = models.BooleanField(default=False)
    reception = models.BooleanField(default=False)
    lobby = models.BooleanField(default=False)
    concierge = models.BooleanField(default=False)
    laundry_room = models.BooleanField(default=False)
    play_area = models.BooleanField(default=False, help_text="Children's play area")
    pet_friendly = models.BooleanField(default=False)

    # Staff
    house_staff = models.BooleanField(default=False, help_text="Includes house help/gardener")
    askari = models.BooleanField(default=False, help_text="Watchman/Security guard included")
    caretaker = models.BooleanField(default=False)

    # Pricing
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Price (KES)"
    )
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=None
    )
    price_per_month = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        default=None
    )
    price_per_sqm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    # Additional costs
    service_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Monthly service charge (KES)"
    )
    deposit_required = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    utilities_included = models.BooleanField(default=False, help_text="Are utilities included in rent?")

    # For sale only
    title_deed = models.BooleanField(default=False, help_text="Title deed available")
    loan_available = models.BooleanField(default=False, help_text="Financing/Loan available")

    # Images
    main_image = models.ImageField(upload_to='listings/main/')
    image_2 = models.ImageField(upload_to='listings/extra/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='listings/extra/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='listings/extra/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='listings/extra/', blank=True, null=True)
    image_6 = models.ImageField(upload_to='listings/extra/', blank=True, null=True)
    image_7 = models.ImageField(upload_to='listings/extra/', blank=True, null=True)
    image_8 = models.ImageField(upload_to='listings/extra/', blank=True, null=True)

    # Virtual Tour
    virtual_tour_url = models.URLField(blank=True, null=True, help_text="Link to 3D tour/video walkthrough")
    youtube_video_id = models.CharField(max_length=50, blank=True, null=True, help_text="YouTube video ID")

    # Map & Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    whatsapp_group_link = models.URLField(blank=True, null=True, help_text="Link to WhatsApp group for inquiries")

    # Status & Dates
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False, help_text="Property has been physically verified")
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Available dates
    available_from = models.DateField(blank=True, null=True)
    available_to = models.DateField(blank=True, null=True)
    minimum_stay = models.PositiveIntegerField(default=1, blank=True, null=True,
                                               help_text="Minimum number of nights/days")
    maximum_stay = models.PositiveIntegerField(default=365, blank=True, null=True,
                                               help_text="Maximum number of nights/days")

    # User relationship
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_listings',
        verbose_name='Property Owner',
        null=True,
        blank=True
    )

    # Meta
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        listing_type_display = "Featured" if self.is_featured else "Free"
        return f"[{listing_type_display}] {self.title} - {self.location}"

    def save(self, *args, **kwargs):
        # Automatically set is_featured based on listing_type
        self.is_featured = (self.listing_type == 'featured')

        # Auto-fill host_email from user if not set
        if self.user and not self.host_email:
            self.host_email = self.user.email

        # Auto-fill host_name from user if not set
        if self.user and not self.host_name:
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
            self.host_name = full_name if full_name else self.user.username

        # Set price_per_night or price_per_month based on transaction_type
        if self.transaction_type == 'shortlet' and self.price and not self.price_per_night:
            self.price_per_night = self.price
        elif self.transaction_type == 'rent' and self.price and not self.price_per_month:
            self.price_per_month = self.price
        elif self.transaction_type == 'sale' and self.price and not self.price:
            self.price = self.price

        if not self.slug:
            from django.utils.text import slugify
            import uuid
            self.slug = slugify(f"{self.title}-{uuid.uuid4().hex[:8]}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('listing_detail', kwargs={'slug': self.slug})

    def whatsapp_link(self):
        return f"https://wa.me/{self.host_whatsapp.replace('+', '')}"

    def call_link(self):
        return f"tel:{self.host_phone}"

    def admin_whatsapp_link(self):
        """WhatsApp link with admin number and booking message"""
        message = f"Hello! I'd like to inquire about this property:\n"
        message += f"Property: {self.title}\n"
        message += f"Location: {self.get_location_display()} - {self.specific_location}\n"
        message += f"Host: {self.host_name}\n"

        if self.transaction_type == 'shortlet' and self.price_per_night:
            message += f"Price: KSh {self.price_per_night}/night\n"
        elif self.transaction_type == 'rent' and self.price_per_month:
            message += f"Price: KSh {self.price_per_month}/month\n"
        elif self.price:
            message += f"Price: KSh {self.price}\n"

        message += f"Property Type: {self.get_property_type_display()}\n"
        message += f"Listing Type: {self.get_listing_type_display()}\n\n"

        import urllib.parse
        encoded_message = urllib.parse.quote(message)

        return f"https://wa.me/{self.admin_contact.replace('+', '')}?text={encoded_message}"

    def admin_call_link(self):
        """Direct call link to admin number"""
        return f"tel:{self.admin_contact}"

    @property
    def all_images(self):
        """Get all images for this listing as a list"""
        images = []
        if self.main_image:
            images.append(self.main_image)
        if self.image_2:
            images.append(self.image_2)
        if self.image_3:
            images.append(self.image_3)
        if self.image_4:
            images.append(self.image_4)
        if self.image_5:
            images.append(self.image_5)
        if self.image_6:
            images.append(self.image_6)
        if self.image_7:
            images.append(self.image_7)
        if self.image_8:
            images.append(self.image_8)
        return images

    @property
    def image_count(self):
        """Get the total number of images for this listing"""
        count = 0
        if self.main_image:
            count += 1
        if self.image_2:
            count += 1
        if self.image_3:
            count += 1
        if self.image_4:
            count += 1
        if self.image_5:
            count += 1
        if self.image_6:
            count += 1
        if self.image_7:
            count += 1
        if self.image_8:
            count += 1
        return count

    @property
    def has_multiple_images(self):
        """Check if listing has more than one image"""
        return self.image_count > 1

    @property
    def listing_type_display(self):
        """Get formatted listing type"""
        return "Featured" if self.listing_type == 'featured' else "Free"

    @property
    def is_paid_featured(self):
        """Check if this is a paid featured listing"""
        return self.listing_type == 'featured'

    @property
    def featured_price_display(self):
        """Display formatted featured price"""
        return f"KES {self.featured_payment_amount:,.2f}"

    @property
    def formatted_price(self):
        """Get formatted price based on transaction type"""
        if self.transaction_type == 'shortlet' and self.price_per_night:
            return f"KES {self.price_per_night:,.0f}/night"
        elif self.transaction_type == 'rent' and self.price_per_month:
            return f"KES {self.price_per_month:,.0f}/month"
        elif self.transaction_type == 'sale' and self.price:
            return f"KES {self.price:,.0f}"
        else:
            return "Price on request"

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = "Property Listing"
        verbose_name_plural = "Property Listings"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    INQUIRY_TYPE_CHOICES = [
        ('general', 'General Inquiry'),
        ('booking', 'Booking Request'),
        ('viewing', 'Schedule Viewing'),
        ('price', 'Price Negotiation'),
        ('other', 'Other'),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)

    # Simplified fields - removed dates and guest count
    message = models.TextField(blank=True, help_text="Guest's message or inquiry")
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES, default='general')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional: Store the property price at time of inquiry for reference
    price_at_inquiry = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # User relationship for booking history
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_bookings',
        verbose_name='Guest Account'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Property Inquiry'
        verbose_name_plural = 'Property Inquiries'

    def __str__(self):
        return f"Inquiry #{self.id} - {self.guest_name} - {self.listing.title}"

    def save(self, *args, **kwargs):
        # Store the current price when inquiry is created
        if not self.price_at_inquiry and self.listing:
            if self.listing.transaction_type == 'shortlet' and self.listing.price_per_night:
                self.price_at_inquiry = self.listing.price_per_night
            elif self.listing.price:
                self.price_at_inquiry = self.listing.price
        super().save(*args, **kwargs)

    @property
    def inquiry_ref(self):
        """Generate inquiry reference number"""
        return f"INQ{self.id:06d}"