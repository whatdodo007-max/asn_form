from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "ASN FARMS Admin"
admin.site.site_title = "ASN FARMS"
admin.site.index_title = "Manage listings, enquiries and messages"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("market.urls")),
]

# Serve uploaded images when running locally (DEBUG). On a host, map /media/ instead.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
