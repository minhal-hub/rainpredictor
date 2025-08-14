from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path('prediction/', include('prediction.urls')),\
    path('', RedirectView.as_view(pattern_name='prediction:index', permanent=False)),
]
