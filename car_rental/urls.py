# car_rental/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rental import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # App URLs
    path('', views.home, name='home'),
    path('rental/', include('rental.urls')),
    # (you can remove the explicit car-list & rentals here if they're already
    #  in rental/urls.py under the 'rental/' prefix)
]

# During development only: serve uploaded media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)