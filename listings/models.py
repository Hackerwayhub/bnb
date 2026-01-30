from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings


class Listing(models.Model):
    PROPERTY_TYPES = [
        ('studio', 'Studio'),
        ('one_bedroom', 'One Bedroom'),
        ('two_bedroom', 'Two Bedroom'),
        ('three_bedroom', 'Three Bedroom'),
        ('Own_compound', 'Own compound'),
        ('beach_house', 'beach house'),
    ]

    LOCATIONS = [
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

    # Property Details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # Added blank=True since it's not in form
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    location = models.CharField(max_length=100, choices=LOCATIONS)
    specific_location = models.CharField(max_length=200, help_text="Specific area/estate")

    # Contact Information
    host_name = models.CharField(max_length=100)

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+254712345678'"
    )

    host_phone = models.CharField(max_length=15, validators=[phone_validator])
    host_whatsapp = models.CharField(max_length=15, validators=[phone_validator])

    # Default admin contact (prefilled, not editable by users)
    admin_contact = models.CharField(
        max_length=15,
        default='+254707341748',
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

    # Property Features
    guests = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    beds = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()

    # Amenities (as Boolean fields)
    wifi = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)

    # Pricing
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    # Images
    main_image = models.ImageField(upload_to='listings/main/')
    image_2 = models.ImageField(upload_to='listings/extra/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='listings/extra/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='listings/extra/', blank=True, null=True)

    # Status & Dates
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Meta
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        listing_type_display = "Featured" if self.is_featured else "Free"
        return f"[{listing_type_display}] {self.title} - {self.location}"

    def save(self, *args, **kwargs):
        # Automatically set is_featured based on listing_type
        self.is_featured = (self.listing_type == 'featured')

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
        message = f"Hello! I'd like to book this bnb:\n"
        message += f"Property: {self.title}\n"
        message += f"Location: {self.get_location_display()} - {self.specific_location}\n"
        message += f"Host: {self.host_name}\n"
        message += f"code: {self.host_phone}\n"
        message += f"Price: KSh {self.price_per_night}/night\n"
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

    class Meta:
        ordering = ['-is_featured', '-created_at']  # Featured listings first
        verbose_name = "Property Listing"
        verbose_name_plural = "Property Listings"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id} - {self.listing.title}"

    def save(self, *args, **kwargs):
        # Calculate total price based on number of nights
        if self.check_in and self.check_out:
            nights = (self.check_out - self.check_in).days
            if nights > 0:
                self.total_price = self.listing.price_per_night * nights
        super().save(*args, **kwargs)

    @property
    def number_of_nights(self):
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return 0