from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from G4Marketplace import settings

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('item/', include('item.urls')),
    path('inbox/', include('conversation.urls')),
    path('verification/', include('verify_email.urls')),
    path('profile/', include('profile.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
               + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
