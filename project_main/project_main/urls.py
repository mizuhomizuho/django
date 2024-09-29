"""
URL configuration for project_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app_main.views import AppMainView
from project_main import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AppMainView.index, name='frontpage'),
    path('simple-form/', AppMainView.simple_form, name='simple_form'),
    path('clear-cache/', AppMainView.clear_cache, name='clear_cache'),
    path('catalog/', include('app_catalog.urls')),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = AppMainView.page_not_found

admin.site.site_header = 'Meow Admin'
admin.site.index_title = 'Meow Meow Admin'