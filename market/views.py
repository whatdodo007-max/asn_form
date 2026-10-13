from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm, InquiryForm, ListingForm
from .models import Listing

SESSION_KEY = "unlocked_listings"


def _unlocked_ids(request):
    return set(request.session.get(SESSION_KEY, []))


def _filtered_listings(request):
    qs = Listing.objects.filter(is_active=True)
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    place = request.GET.get("place", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(seller_name__icontains=q))
    if category in dict(Listing.CATEGORY_CHOICES):
        qs = qs.filter(category=category)
    if place:
        qs = qs.filter(location__icontains=place)
    if max_price:
        try:
            qs = qs.filter(price__lte=float(max_price))
        except ValueError:
            pass
    return qs


def _page(request, qs, per_page=12):
    return Paginator(qs, per_page).get_page(request.GET.get("page"))


def _querystring_without_page(request):
    params = request.GET.copy()
    params.pop("page", None)
    return params.urlencode()


def home(request):
    active = Listing.objects.filter(is_active=True)
    counts = dict(active.values_list("category").annotate(n=Count("id")))
    categories = [
        {"key": key, "label": label, "count": counts.get(key, 0)}
        for key, label in Listing.CATEGORY_CHOICES
    ]
    return render(
        request,
        "market/home.html",
        {
            "latest": active[:6],
            "categories": categories,
            "total_items": active.count(),
            "total_places": active.values("location").distinct().count(),
        },
    )


def buyer(request):
    page = _page(request, _filtered_listings(request))
    return render(
        request,
        "market/buyer.html",
        {
            "page": page,
            "categories": Listing.CATEGORY_CHOICES,
            "filters": request.GET,
            "qs": _querystring_without_page(request),
            "section": "buyer",
        },
    )


def seller(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your item is now live! Buyers can see it in the list below.")
            return redirect("seller")
        messages.error(request, "Please fix the highlighted fields and try again.")
    else:
        form = ListingForm()

    page = _page(request, _filtered_listings(request), per_page=9)
    return render(
        request,
        "market/seller.html",
        {
            "form": form,
            "page": page,
            "categories": Listing.CATEGORY_CHOICES,
            "filters": request.GET,
            "qs": _querystring_without_page(request),
            "section": "seller",
        },
    )


def detail(request, pk):
    """Seller card page. The mobile number is only sent to the browser after unlock."""
    listing = get_object_or_404(Listing, pk=pk, is_active=True)
    unlocked = listing.pk in _unlocked_ids(request)
    context = {
        "listing": listing,
        "unlocked": unlocked,
        "form": None if unlocked else InquiryForm(),
    }
    if request.method == "POST" and not unlocked:
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.listing = listing
            inquiry.save()
            ids = _unlocked_ids(request)
            ids.add(listing.pk)
            request.session[SESSION_KEY] = list(ids)
            messages.success(request, "Thank you! The seller's mobile number is shown below.")
            return redirect("detail", pk=pk)
        context["form"] = form
    related = (
        Listing.objects.filter(is_active=True, category=listing.category).exclude(pk=pk)[:3]
    )
    context["related"] = related
    return render(request, "market/detail.html", context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent! We will get back to you soon.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "market/contact.html", {"form": form, "section": "contact"})
