import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('accueil/', include('main_page.urls')),
    path('velouse/', include('velouse.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='velouse/')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]