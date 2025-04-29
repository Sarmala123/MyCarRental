# car_rental/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rental import views  # Add this import to fix the error

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),
    
    # Home page route (root URL)
    path('', views.home, name='home'),  # This maps the root URL to the 'home' view
    
    # Include rental app URLs
    path('rental/', include('rental.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)