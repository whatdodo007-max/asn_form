from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("buyer/", views.buyer, name="buyer"),
    path("seller/", views.seller, name="seller"),
    path("item/<int:pk>/", views.detail, name="detail"),
    path("contact/", views.contact, name="contact"),
]
