from django.contrib import admin
from django.utils.html import format_html
from .models import Listing, Booking


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'property_type', 'location', 'price_per_night',
                    'listing_type_display', 'is_approved', 'is_featured', 'created_at')
    list_filter = ('is_approved', 'is_featured', 'listing_type', 'property_type', 'location', 'user')
    search_fields = ('title', 'description', 'host_name', 'specific_location', 'user__username', 'user__email')
    list_editable = ('is_approved', 'is_featured')
    readonly_fields = ('created_at', 'updated_at', 'slug', 'featured_payment_amount')
    raw_id_fields = ('user',)

    # Add actions for bulk operations
    actions = ['make_featured', 'make_free', 'approve_listings', 'unapprove_listings']

    fieldsets = (
        ('Property Details', {
            'fields': ('title', 'description', 'property_type', 'location',
                       'specific_location', 'slug')
        }),
        ('Contact Information', {
            'fields': ('host_name', 'host_email', 'host_phone', 'host_whatsapp', 'admin_contact')
        }),
        ('Listing Type & Pricing', {
            'fields': ('listing_type', 'featured_payment_amount', 'price_per_night')
        }),
        ('Property Features', {
            'fields': ('guests', 'bedrooms', 'beds', 'bathrooms')
        }),
        ('Amenities', {
            'fields': ('wifi', 'parking', 'kitchen', 'pool', 'ac', 'tv')
        }),
        ('Images', {
            'fields': ('main_image', 'image_2', 'image_3', 'image_4')
        }),
        ('Status & User', {
            'fields': ('user', 'is_approved', 'is_featured', 'created_at', 'updated_at')
        }),
    )

    def listing_type_display(self, obj):
        """Display listing type in admin list"""
        return obj.get_listing_type_display()

    listing_type_display.short_description = 'Listing Type'
    listing_type_display.admin_order_field = 'listing_type'

    def make_featured(self, request, queryset):
        """Action to make listings featured"""
        updated = queryset.update(listing_type='featured', is_featured=True, featured_payment_amount=1000.00)
        self.message_user(request, f'{updated} listing(s) marked as featured.')

    make_featured.short_description = "Mark selected listings as Featured"

    def make_free(self, request, queryset):
        """Action to make listings free"""
        updated = queryset.update(listing_type='free', is_featured=False, featured_payment_amount=0.00)
        self.message_user(request, f'{updated} listing(s) marked as free.')

    make_free.short_description = "Mark selected listings as Free"

    def approve_listings(self, request, queryset):
        """Action to approve listings"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} listing(s) approved.')

    approve_listings.short_description = "Approve selected listings"

    def unapprove_listings(self, request, queryset):
        """Action to unapprove listings"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} listing(s) unapproved.')

    unapprove_listings.short_description = "Unapprove selected listings"

    def get_form(self, request, obj=None, **kwargs):
        """Customize the form to show help text for featured payment"""
        form = super().get_form(request, obj, **kwargs)
        if 'featured_payment_amount' in form.base_fields:
            form.base_fields[
                'featured_payment_amount'].help_text = "KES 1000 for featured listings, 0 for free listings"
        return form


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest_name', 'user', 'listing_link', 'check_in', 'check_out',
                    'number_of_guests', 'total_price', 'status_badge', 'created_at', 'contact_info')
    list_filter = ('status', 'check_in', 'check_out', 'listing', 'created_at', 'user')
    search_fields = ('guest_name', 'guest_email', 'guest_phone', 'listing__title', 'user__username')
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'total_price_display', 'duration_display')
    ordering = ('-created_at',)
    raw_id_fields = ('listing', 'user')

    fieldsets = (
        ('Booking Information', {
            'fields': ('listing', 'user', 'status', 'total_price_display')
        }),
        ('Guest Information', {
            'fields': ('guest_name', 'guest_email', 'guest_phone')
        }),
        ('Stay Details', {
            'fields': ('check_in', 'check_out', 'duration_display', 'number_of_guests')
        }),
        ('Additional Information', {
            'fields': ('special_requests',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Add custom actions
    actions = ['mark_as_confirmed', 'mark_as_pending', 'mark_as_cancelled', 'mark_as_completed']

    def listing_link(self, obj):
        url = f"/admin/listings/listing/{obj.listing.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.listing.title)

    listing_link.short_description = 'Property'
    listing_link.admin_order_field = 'listing__title'

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'green',
            'cancelled': 'red',
            'completed': 'blue',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )

    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    def contact_info(self, obj):
        return format_html(
            '📧 {}<br>📱 {}',
            obj.guest_email,
            obj.guest_phone
        )

    contact_info.short_description = 'Contact'

    def total_price_display(self, obj):
        return format_html('<strong>KES {}</strong>', obj.total_price)

    total_price_display.short_description = 'Total Price'

    def duration_display(self, obj):
        if obj.check_in and obj.check_out:
            nights = (obj.check_out - obj.check_in).days
            return f"{nights} night(s)"
        return "N/A"

    duration_display.short_description = 'Duration'

    # Custom action methods
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} booking(s) marked as confirmed.')

    mark_as_confirmed.short_description = "✅ Mark selected as confirmed"

    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} booking(s) marked as pending.')

    mark_as_pending.short_description = "⏳ Mark selected as pending"

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} booking(s) marked as cancelled.')

    mark_as_cancelled.short_description = "❌ Mark selected as cancelled"

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} booking(s) marked as completed.')

    mark_as_completed.short_description = "✅ Mark selected as completed"

    def get_queryset(self, request):
        # Add related listing to optimize queries
        return super().get_queryset(request).select_related('listing', 'user')

    # Customize form to show relevant help text
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['status'].help_text = "Change booking status here"
        form.base_fields['special_requests'].widget.attrs['rows'] = 3
        return form