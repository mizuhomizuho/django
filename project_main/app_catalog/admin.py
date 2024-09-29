from django.contrib import admin, messages
from django.db.models import Count
from django.utils.safestring import mark_safe

from .models import Sections, Elements

class EmptySectionsFilter(admin.SimpleListFilter):
    title = 'Не пустые категории'
    parameter_name = 'empty_sections'

    def lookups(self, request, model_admin):
        return [
            ('empty', 'Empty'),
            ('no_empty', 'No empty'),
        ]

    def queryset(self, request, queryset):
        queryset_filter = queryset.annotate(count_elements=Count('elements'))
        if self.value() == 'empty':
            return queryset_filter.filter(count_elements__gt=0)
        elif self.value() == 'no_empty':
            return queryset_filter.filter(count_elements__lt=1)

# admin.site.register(Sections, SectionsAdmin)
@admin.register(Sections)
class SectionsAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'time_created', 'is_active', 'short_info')
    list_display_links = ('name',)
    ordering = ['-time_created', 'name']
    list_editable = ('sort', 'is_active')
    actions = ['set_active', 'set_no_active']
    search_fields = ('id', 'name__startswith', 'elements__name')
    list_filter = (EmptySectionsFilter,)

    @admin.display(ordering='name', description='Name len')
    def short_info(self, section: Sections):
        return f'Len: {len(section.name)}'

    @admin.action(description='Active on')
    def set_active(self, request, queryset):
        count = queryset.update(is_active=Sections.Status.ACTIVE)
        self.message_user(request, f'Cange {count}')

    @admin.action(description='Active off')
    def set_no_active(self, request, queryset):
        count = queryset.update(is_active=Sections.Status.NO_ACTIVE)
        self.message_user(request, f'Cange {count}', messages.WARNING)

@admin.register(Elements)
class ElementsAdmin(admin.ModelAdmin):
    # exclude = ['sort'] # исключить поля из формы редактирования
    # readonly_fields =
    filter_horizontal = ('sections',) # для замены обычного <select>
    # filter_vertical = ('sections',) # тоже что и filter_horizontal
    prepopulated_fields = {'code': ('name',)}
    fields = ['name', 'code', 'sections', 'photo'] # поля формы редактирования
    list_display = ('photo_html', 'name', 'sort', 'code', 'time_created', 'is_active')
    list_display_links = ('photo_html', 'name')
    ordering = ['-time_created', '-time_updated']
    list_editable = ('sort', 'is_active')
    list_per_page = 8
    list_filter = ('sort', 'is_active', 'name', 'sections')

    @admin.display(description='Картинка')
    def photo_html(self, item: Elements):
        if item.photo:
            return mark_safe(f'<img src="{item.photo.url}" style="max-width: 88px;width: 100%;height: auto">')
        else:
            return ''
