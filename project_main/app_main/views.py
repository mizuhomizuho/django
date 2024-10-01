from PIL import Image
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseNotFound
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from app_catalog.models import Sections
from app_main.forms import SimpleForm

class Views:

    @staticmethod
    def page_not_found(request, exception) -> None:
        return HttpResponseNotFound('Page not found.')

    @staticmethod
    def index(request) -> None:

        data = {
            'seo': {
                'title': 'Site catalog',
                'description': 'Site catalog',
            },
            'h1': '<b style="color: #d35350">H</b>ellow',
            'csrf_token': get_token(request),
        }

        str = render_to_string('app_main/index.html', data)
        return HttpResponse(str)

    @staticmethod
    def clear_cache(request) -> None:
        cache.clear()
        return HttpResponse('<script>window.history.back()</script>')

    @staticmethod
    def __handle_uploaded_file(f) -> None:
        # import uuid
        with open(f'uploads/{f.name}', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    @staticmethod
    def __validate_image(image) -> None:
        try:
            img = Image.open(image)
            if img.format.lower() not in ['jpeg', 'jpg', 'png']:
                raise ValidationError('Invalid image format')
        except:
            raise ValidationError('Invalid image')

    @classmethod
    def simple_form(cls, request) -> None:
        good_msg = ''
        if request.POST.get('form_id') == 'form_simple':
            form = SimpleForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    for img in request.FILES.getlist('files_img'):
                        cls.__validate_image(img)
                    data_for_add = form.cleaned_data
                    del data_for_add['files_img']
                    Sections.objects.create(**data_for_add)
                    for img in request.FILES.getlist('files_img'):
                        cls.__handle_uploaded_file(img)
                    form = SimpleForm()
                    good_msg = 'Успешно'
                except Exception as e:
                    form.add_error(None, f'Ошибка добавления {e.args[0]}')
        else:
            form = SimpleForm()
        return render(request, 'app_main/simple_form.html', {
            'form': form,
            'good_msg': good_msg,
        })

class TemplateViewPage(TemplateView):

    template_name = 'app_main/template_view_page.html'
    # extra_context = {
    #     'text': 'Meow...'
    # }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = f'Cat said {self.request.GET.get('meow', 'yes')}'
        return context