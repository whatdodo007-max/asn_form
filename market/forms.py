import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from .models import ContactMessage, Inquiry, Listing

MAX_IMAGE_MB = 5


def clean_indian_mobile(value):
    """Accepts 9876543210, +91 98765 43210, 098765-43210 ... returns 10 digits."""
    digits = re.sub(r"\D", "", value or "")
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) == 11:
        digits = digits[1:]
    if not re.fullmatch(r"[6-9]\d{9}", digits):
        raise ValidationError("Enter a valid 10-digit Indian mobile number.")
    return digits


class StyledFormMixin:
    # Fields that hold a mobile number. Users may type "+91 98765 43210", which is
    # longer than the 10 digits we store, so the DB max_length must not reject it
    # before clean_indian_mobile() normalises it.
    mobile_fields = ("mobile", "visitor_mobile")

    def _style(self):
        for name in self.mobile_fields:
            field = self.fields.get(name)
            if field is not None:
                field.max_length = 20
                field.validators = [
                    v for v in field.validators if not isinstance(v, MaxLengthValidator)
                ]
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.ClearableFileInput):
                widget.attrs.setdefault("accept", "image/*")
            widget.attrs.setdefault("class", "input")


class ListingForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "seller_name",
            "title",
            "category",
            "image",
            "price",
            "price_note",
            "location",
            "mobile",
            "description",
        ]
        widgets = {
            "seller_name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "title": forms.TextInput(attrs={"placeholder": "e.g. Healthy Jersey cow, Country eggs"}),
            "price": forms.NumberInput(attrs={"placeholder": "Price in ₹", "min": "0", "step": "0.01"}),
            "price_note": forms.TextInput(attrs={"placeholder": "per kg / per piece"}),
            "location": forms.TextInput(attrs={"placeholder": "Village, District"}),
            "mobile": forms.TextInput(
                attrs={"placeholder": "10-digit mobile", "inputmode": "numeric", "maxlength": "15"}
            ),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Age, quality, quantity... (optional)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = [("", "Choose category")] + list(Listing.CATEGORY_CHOICES)
        self._style()

    def clean_mobile(self):
        return clean_indian_mobile(self.cleaned_data["mobile"])

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise ValidationError("Price cannot be negative.")
        return price

    def clean_image(self):
        image = self.cleaned_data["image"]
        if image and image.size > MAX_IMAGE_MB * 1024 * 1024:
            raise ValidationError(f"Image is too large. Max {MAX_IMAGE_MB} MB.")
        return image


class InquiryForm(StyledFormMixin, forms.ModelForm):
    """Visitor fills this to unlock ONE seller's mobile number."""

    class Meta:
        model = Inquiry
        fields = ["visitor_name", "visitor_mobile", "visitor_place"]
        labels = {
            "visitor_name": "Your name",
            "visitor_mobile": "Your mobile number",
            "visitor_place": "Your village / town (optional)",
        }
        widgets = {
            "visitor_name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "visitor_mobile": forms.TextInput(
                attrs={"placeholder": "10-digit mobile", "inputmode": "numeric", "maxlength": "15"}
            ),
            "visitor_place": forms.TextInput(attrs={"placeholder": "Village / Town"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    def clean_visitor_mobile(self):
        return clean_indian_mobile(self.cleaned_data["visitor_mobile"])


class ContactForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "mobile", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email (optional)"}),
            "mobile": forms.TextInput(
                attrs={"placeholder": "Mobile (optional)", "inputmode": "numeric", "maxlength": "15"}
            ),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "How can we help?"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    def clean_mobile(self):
        value = self.cleaned_data.get("mobile", "")
        return clean_indian_mobile(value) if value.strip() else ""

    def clean(self):
        data = super().clean()
        if not data.get("email") and not data.get("mobile"):
            raise ValidationError("Please give an email or a mobile number so we can reply.")
        return data
