# bnbke/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap
from listings.sitemaps import sitemaps
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('listings.urls')),
    path('auth/', include('auth.urls')),
path('accounts/', RedirectView.as_view(url='/auth/login/', permanent=True)),
    path('accounts/profile/', RedirectView.as_view(url='/auth/profile/', permanent=True)),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain')
    ),

]

# Serve static files during development
urlpatterns += staticfiles_urlpatterns()

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# For production, you'll need to configure your web server (nginx/apache)