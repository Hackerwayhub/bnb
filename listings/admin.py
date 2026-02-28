from django.contrib import admin
from django.utils.html import format_html
from .models import Listing, Booking


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'transaction_type', 'property_type', 'location',
                    'price_display', 'listing_type_display', 'is_approved', 'is_featured',
                    'is_verified', 'bedrooms', 'bathrooms', 'views_count', 'created_at')
    list_filter = ('is_approved', 'is_featured', 'is_verified', 'listing_type', 'transaction_type',
                   'property_type', 'location', 'condition', 'furnishing', 'user', 'created_at')
    search_fields = ('title', 'description', 'host_name', 'host_email', 'specific_location',
                     'address', 'user__username', 'user__email')
    list_editable = ('is_approved', 'is_featured', 'is_verified')
    readonly_fields = ('created_at', 'updated_at', 'slug', 'featured_payment_amount',
                       'views_count', 'image_count_display', 'formatted_price')
    raw_id_fields = ('user',)
    list_per_page = 25
    date_hierarchy = 'created_at'

    # Add actions for bulk operations
    actions = ['make_featured', 'make_free', 'approve_listings', 'unapprove_listings',
               'mark_as_verified', 'bulk_export']

    fieldsets = (
        # Basic Information
        ('Basic Information', {
            'fields': ('title', 'description', 'property_type', 'transaction_type',
                       'location', 'specific_location', 'address', 'slug')
        }),

        # Contact Information
        ('Contact Information', {
            'fields': ('host_name', 'host_email', 'host_phone', 'host_whatsapp', 'admin_contact')
        }),

        # Listing Type & Pricing
        ('Listing Type & Pricing', {
            'fields': ('listing_type', 'featured_payment_amount', 'price', 'price_per_night',
                       'price_per_month', 'price_per_sqm', 'formatted_price')
        }),

        # Additional Costs
        ('Additional Costs', {
            'fields': ('service_charge', 'deposit_required', 'utilities_included')
        }),

        # Property Size
        ('Property Size', {
            'fields': ('land_size', 'land_size_unit', 'floor_area')
        }),

        # Rooms & Capacity
        ('Rooms & Capacity', {
            'fields': ('guests', 'bedrooms', 'beds', 'bathrooms', 'en_suites',
                       'living_rooms', 'dining_rooms', 'kitchens')
        }),

        # Property Condition
        ('Property Condition', {
            'fields': ('year_built', 'condition', 'furnishing')
        }),

        # Floor Details
        ('Floor Details', {
            'fields': ('total_floors', 'floor_number')
        }),

        # Parking
        ('Parking', {
            'fields': ('parking_spots', 'covered_parking', 'visitor_parking')
        }),

        # Basic Amenities
        ('Basic Amenities', {
            'fields': ('wifi', 'parking', 'kitchen')
        }),

        # Fitness & Wellness
        ('Fitness & Wellness', {
            'fields': ('gym', 'pool', 'spa', 'sauna', 'steam_room'),
            'classes': ('collapse',)
        }),

        # Climate Control
        ('Climate Control', {
            'fields': ('ac', 'heating', 'ceiling_fans', 'fireplace'),
            'classes': ('collapse',)
        }),

        # Entertainment
        ('Entertainment', {
            'fields': ('tv', 'sound_system', 'home_theater'),
            'classes': ('collapse',)
        }),

        # Outdoor Features
        ('Outdoor Features', {
            'fields': ('balcony', 'terrace', 'garden', 'roof_terrace', 'bbq_area', 'outdoor_shower'),
            'classes': ('collapse',)
        }),

        # Security
        ('Security', {
            'fields': ('cctv', 'security_guards', 'electric_fence', 'secure_compound', 'alarm_system'),
            'classes': ('collapse',)
        }),

        # Utilities
        ('Utilities', {
            'fields': ('generator', 'solar_panels', 'water_tank', 'borehole', 'backup_water', 'internet_fiber'),
            'classes': ('collapse',)
        }),

        # Building Amenities
        ('Building Amenities', {
            'fields': ('elevator', 'wheelchair_accessible', 'reception', 'lobby', 'concierge',
                       'laundry_room', 'play_area', 'pet_friendly'),
            'classes': ('collapse',)
        }),

        # Staff
        ('Staff', {
            'fields': ('house_staff', 'askari', 'caretaker'),
            'classes': ('collapse',)
        }),

        # Additional Features
        ('Additional Features', {
            'fields': ('servant_quarters', 'store_rooms', 'title_deed', 'loan_available')
        }),

        # Availability
        ('Availability', {
            'fields': ('available_from', 'available_to', 'minimum_stay', 'maximum_stay')
        }),

        # Media
        ('Media', {
            'fields': ('main_image', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6',
                       'image_7', 'image_8', 'virtual_tour_url', 'youtube_video_id', 'image_count_display')
        }),

        # Map & Location
        ('Map & Location', {
            'fields': ('latitude', 'longitude', 'whatsapp_group_link')
        }),

        # Status & User
        ('Status & User', {
            'fields': ('user', 'is_approved', 'is_featured', 'is_verified', 'views_count',
                       'created_at', 'updated_at')
        }),
    )

    def listing_type_display(self, obj):
        """Display listing type in admin list"""
        colors = {
            'free': '#6c757d',
            'featured': '#ffc107',
        }
        color = colors.get(obj.listing_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, 'black' if obj.listing_type == 'featured' else 'white',
            obj.get_listing_type_display()
        )

    listing_type_display.short_description = 'Listing Type'
    listing_type_display.admin_order_field = 'listing_type'

    def price_display(self, obj):
        """Display formatted price in admin list"""
        if obj.transaction_type == 'shortlet' and obj.price_per_night:
            return format_html('<strong>KES {}/night</strong>', obj.price_per_night)
        elif obj.transaction_type == 'rent' and obj.price_per_month:
            return format_html('<strong>KES {}/month</strong>', obj.price_per_month)
        elif obj.price:
            return format_html('<strong>KES {}</strong>', obj.price)
        return 'Price on request'

    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'

    def formatted_price(self, obj):
        """Read-only field showing formatted price"""
        return obj.formatted_price

    formatted_price.short_description = 'Formatted Price'

    def image_count_display(self, obj):
        """Display number of images"""
        count = obj.image_count
        color = 'green' if count >= 5 else ('orange' if count >= 3 else 'red')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} image(s)</span>',
            color, count
        )

    image_count_display.short_description = 'Images'

    def make_featured(self, request, queryset):
        """Action to make listings featured"""
        updated = queryset.update(listing_type='featured', is_featured=True, featured_payment_amount=1000.00)
        self.message_user(request, f'{updated} listing(s) marked as featured.')

    make_featured.short_description = "⭐ Mark selected as Featured"

    def make_free(self, request, queryset):
        """Action to make listings free"""
        updated = queryset.update(listing_type='free', is_featured=False, featured_payment_amount=0.00)
        self.message_user(request, f'{updated} listing(s) marked as free.')

    make_free.short_description = "🆓 Mark selected as Free"

    def approve_listings(self, request, queryset):
        """Action to approve listings"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} listing(s) approved.')

    approve_listings.short_description = "✅ Approve selected listings"

    def unapprove_listings(self, request, queryset):
        """Action to unapprove listings"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} listing(s) unapproved.')

    unapprove_listings.short_description = "❌ Unapprove selected listings"

    def mark_as_verified(self, request, queryset):
        """Action to mark listings as verified"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} listing(s) marked as verified.')

    mark_as_verified.short_description = "✓ Mark selected as Verified"

    def bulk_export(self, request, queryset):
        """Action to export selected listings (placeholder)"""
        self.message_user(request, f'{queryset.count()} listing(s) ready for export. (Export feature coming soon)')

    bulk_export.short_description = "📤 Export selected listings"

    def get_form(self, request, obj=None, **kwargs):
        """Customize the form to show help text"""
        form = super().get_form(request, obj, **kwargs)

        # Add help text for featured payment
        if 'featured_payment_amount' in form.base_fields:
            form.base_fields[
                'featured_payment_amount'].help_text = "KES 1000 for featured listings, 0 for free listings"

        # Add help text for transaction type
        if 'transaction_type' in form.base_fields:
            form.base_fields[
                'transaction_type'].help_text = "Select: Rent (monthly), Sale (purchase), or Shortlet (nightly)"

        # Add help text for pricing
        if 'price' in form.base_fields:
            form.base_fields[
                'price'].help_text = "Enter the main price (KES). For shortlet: nightly, rent: monthly, sale: total"

        return form

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user')



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'inquiry_ref', 'guest_name', 'user', 'listing_link',
                    'inquiry_type_display', 'status_badge', 'created_at', 'contact_info')
    list_filter = ('status', 'inquiry_type', 'listing', 'created_at', 'user')
    search_fields = ('guest_name', 'guest_email', 'guest_phone', 'message',
                     'listing__title', 'user__username')
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'inquiry_ref', 'price_at_inquiry_display')
    ordering = ('-created_at',)
    raw_id_fields = ('listing', 'user')

    fieldsets = (
        ('Inquiry Information', {
            'fields': ('inquiry_ref', 'listing', 'user', 'status', 'inquiry_type')
        }),
        ('Guest Information', {
            'fields': ('guest_name', 'guest_email', 'guest_phone')
        }),
        ('Inquiry Details', {
            'fields': ('message', 'price_at_inquiry_display')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Add custom actions
    actions = ['mark_as_confirmed', 'mark_as_pending', 'mark_as_cancelled', 'mark_as_completed']

    def inquiry_ref(self, obj):
        """Display inquiry reference"""
        return obj.inquiry_ref
    inquiry_ref.short_description = 'Reference'
    inquiry_ref.admin_order_field = 'id'

    def inquiry_type_display(self, obj):
        """Display inquiry type with icon"""
        icons = {
            'general': '📝',
            'booking': '📅',
            'viewing': '👁️',
            'price': '💰',
            'other': '❓',
        }
        icon = icons.get(obj.inquiry_type, '📝')
        return format_html('{} {}', icon, obj.get_inquiry_type_display())
    inquiry_type_display.short_description = 'Inquiry Type'
    inquiry_type_display.admin_order_field = 'inquiry_type'

    def listing_link(self, obj):
        """Link to the listing in admin"""
        url = f"/admin/listings/listing/{obj.listing.id}/change/"
        return format_html('<a href="{}" style="font-weight: 500;">{}</a>', url,
                           obj.listing.title[:30] + '...' if len(obj.listing.title) > 30 else obj.listing.title)
    listing_link.short_description = 'Property'
    listing_link.admin_order_field = 'listing__title'

    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'cancelled': '#dc3545',
            'completed': '#17a2b8',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{}</span>',
            color, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    def contact_info(self, obj):
        """Display guest contact information"""
        return format_html(
            '<span style="font-size: 12px;">📧 {}<br>📱 {}</span>',
            obj.guest_email,
            obj.guest_phone
        )
    contact_info.short_description = 'Contact'

    def price_at_inquiry_display(self, obj):
        """Display price at time of inquiry"""
        if obj.price_at_inquiry:
            return format_html('<strong style="color: #28a745;">KES {}</strong>', obj.price_at_inquiry)
        return '-'
    price_at_inquiry_display.short_description = 'Price at Inquiry'

    # Custom action methods
    def mark_as_confirmed(self, request, queryset):
        """Action to mark inquiries as confirmed"""
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'✅ {updated} inquiry/inquiries marked as confirmed.')

    mark_as_confirmed.short_description = "✅ Mark selected as confirmed"

    def mark_as_pending(self, request, queryset):
        """Action to mark inquiries as pending"""
        updated = queryset.update(status='pending')
        self.message_user(request, f'⏳ {updated} inquiry/inquiries marked as pending.')

    mark_as_pending.short_description = "⏳ Mark selected as pending"

    def mark_as_cancelled(self, request, queryset):
        """Action to mark inquiries as cancelled"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'❌ {updated} inquiry/inquiries marked as cancelled.')

    mark_as_cancelled.short_description = "❌ Mark selected as cancelled"

    def mark_as_completed(self, request, queryset):
        """Action to mark inquiries as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'✅ {updated} inquiry/inquiries marked as completed.')

    mark_as_completed.short_description = "✅ Mark selected as completed"

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('listing', 'user')

    def get_form(self, request, obj=None, **kwargs):
        """Customize form fields"""
        form = super().get_form(request, obj, **kwargs)

        # Add help text
        if 'status' in form.base_fields:
            form.base_fields['status'].help_text = "Change inquiry status here"

        if 'message' in form.base_fields:
            form.base_fields['message'].widget.attrs['rows'] = 4
            form.base_fields['message'].help_text = "Guest's message or inquiry"

        return form

    def save_model(self, request, obj, form, change):
        """Override save to handle any notifications"""
        super().save_model(request, obj, form, change)

        # You can add email notification logic here
        if change and 'status' in form.changed_data:
            # Status was changed
            pass