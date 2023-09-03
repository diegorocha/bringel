from django.urls import path, include

from store.api.routes import router
from store.api.swagger import swagger_urls

app_name = 'store'
urlpatterns = [
    path('api/', include(router.urls)),
]
urlpatterns.extend(swagger_urls)
