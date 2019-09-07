from django.contrib import admin
from django.urls import path, include

from core import views, routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(routers.router.urls)),
    path('organizations/<district_pk>/', views.OrganizationsList.as_view())
]
