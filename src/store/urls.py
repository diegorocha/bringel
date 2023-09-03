from django.urls import path, include

from store.api.routes import router

app_name = 'store'
urlpatterns = [
    path('api/', include(router.urls)),
]
