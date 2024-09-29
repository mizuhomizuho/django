from django.urls import path
from app_catalog.views import AppCatalogView

urlpatterns = [
    path('', AppCatalogView.index, name='catalog'),
    path('<path:section_path>/<slug:section_code>/', AppCatalogView.section, name='section'),
    path('<slug:section_code>/', AppCatalogView.section, name='section'),
]
