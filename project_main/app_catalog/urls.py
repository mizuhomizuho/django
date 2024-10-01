from django.urls import path
from app_catalog import views

urlpatterns = [
    path('', views.Views.index, name='catalog'),
    path('add-element/', views.AddElementPage.as_view(), name='add_element_page'),
    path('template-list-view-page/', views.TemplateListViewPage.as_view(), name='template_list_view_page'),
    path('template-detail-view-page/<slug:element_code>/', views.TemplateDetailViewPage.as_view(), name='template_detail_view_page'),
    path('template-form-page/', views.TemplateFormPage.as_view(), name='template_form_page'),
    path('template-create-page/', views.TemplateCreatePage.as_view(), name='template_create_page'),
    path('<path:section_path>/<slug:section_code>/', views.Views.section, name='section'),
    path('<slug:section_code>/', views.Views.section, name='section'),
]
