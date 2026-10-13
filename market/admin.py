from django.contrib import admin
from django.utils.html import format_html

from .models import ContactMessage, Inquiry, Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "category", "price", "location", "seller_name", "mobile", "is_active", "created_at")
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("title", "seller_name", "location", "mobile")
    list_editable = ("is_active",)
    list_display_links = ("thumb", "title")

    @admin.display(description="Photo")
    def thumb(self, obj):
        return format_html('<img src="{}" style="height:44px;border-radius:6px">', obj.image.url) if obj.image else "-"


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("visitor_name", "visitor_mobile", "visitor_place", "listing", "created_at")
    list_filter = ("created_at",)
    search_fields = ("visitor_name", "visitor_mobile", "listing__title")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "mobile", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)
    search_fields = ("name", "subject", "message")
