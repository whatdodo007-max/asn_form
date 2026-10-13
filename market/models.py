from django.db import models


class Listing(models.Model):
    """An item a seller puts up for sale (seller card)."""

    CATEGORY_CHOICES = [
        ("cattle", "Cattle & Goats"),
        ("poultry", "Poultry (Hen, Duck)"),
        ("dairy", "Milk & Dairy"),
        ("vegetables", "Vegetables"),
        ("fruits", "Fruits"),
        ("grains", "Grains & Pulses"),
        ("seeds", "Seeds & Plants"),
        ("tools", "Farm Tools & Equipment"),
        ("other", "Other"),
    ]

    seller_name = models.CharField(max_length=80)
    title = models.CharField("Item name", max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to="listings/%Y/%m/")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_note = models.CharField(
        "Price per", max_length=30, blank=True, help_text="e.g. per kg, per piece, per litre"
    )
    location = models.CharField(max_length=120, help_text="Village / town, district")
    mobile = models.CharField("Mobile number", max_length=10)
    description = models.TextField(blank=True, max_length=600)
    is_active = models.BooleanField(default=True, help_text="Untick to hide this card")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.seller_name} ({self.location})"


class Inquiry(models.Model):
    """Buyer/visitor details captured before a seller's mobile number is revealed."""

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="inquiries")
    visitor_name = models.CharField(max_length=80)
    visitor_mobile = models.CharField(max_length=10)
    visitor_place = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "inquiries"

    def __str__(self):
        return f"{self.visitor_name} -> {self.listing.title}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    subject = models.CharField(max_length=120)
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} - {self.name}"
