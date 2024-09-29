from django.urls import path
from app_catalog.views import Views, AddElementPage

urlpatterns = [
    path('', Views.index, name='catalog'),
    path('add-element/', AddElementPage.as_view(), name='add_element_page'),
    path('<path:section_path>/<slug:section_code>/', Views.section, name='section'),
    path('<slug:section_code>/', Views.section, name='section'),
]
