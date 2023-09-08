from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
