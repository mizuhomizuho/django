from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.core.paginator import Paginator
from app_catalog.models import Sections, Elements
from app_catalog.utils import DataMixin
from app_main.forms import AddElementForm

class Views:

    @staticmethod
    def index(request):

        # Sections.objects.create(name='Cat1', description='Meow1')
        # x1 = Sections.objects.create(name='Cat2', description='Meow2')
        # x2 = Sections.objects.create(name='Cat3', description='Meow3', parent=x1)
        # Sections.objects.create(name='Cat4', description='Meow4', parent=x2)

        # i = 0
        # while True:
        #     if i > 10:
        #         break
        #     new_el = Elements.objects.create(name=f'El {i}', code=f'el-{i}')
        #     new_el.sections.set([14])
        #     # new_el.sections.remove(17, 18)
        #     i += 1

        return render(request, 'app_catalog/index.html', {
            'tree': Sections.tree.get()['tree']
        })

    @staticmethod
    def section(request, section_code, section_path=None):
        section_el = get_object_or_404(Sections, code=section_code)
        items = (
            Elements.objects.filter(sections=section_el).prefetch_related('sections').select_related('author')
        ) # select_related - для OTM и OTO

        p = Paginator(items, 8)
        # p.count
        # p.number
        # p.num_pages
        # p.page_range
        # p.page(1)
        # p.object_list
        # p.has_next()
        # p.has_previous()
        # p.has_other_pages()
        # p.next_page_number()
        # p.previous_page_number()

        pager = p.get_page(request.GET.get('page'))

        # raise Http404()
        # return redirect('section', 'cat1/cat2', 'cat3', permanent=True)
        return render(request, 'app_catalog/section.html', context={
            'tree': Sections.tree.get()['tree'],
            'section': section_el,
            'items': items,
            'pager': pager,
        })

class AddElementPage(View):

    def get(self, request):
        model_form = AddElementForm()
        return render(request, 'app_catalog/add_element_page.html', {
            'model_form': model_form,
        })

    def post(self, request):
        if request.POST.get('form_id') == 'model_form_add_element':
            model_form = AddElementForm(request.POST, request.FILES)
            if model_form.is_valid():
                model_form.save()
        return render(request, 'app_catalog/add_element_page.html', {
            'model_form': model_form,
        })

class TemplateListViewPage(DataMixin, ListView):

    model = Elements
    # template_name = 'xxx/yyy/zzz.html'
    context_object_name = 'my_elements'
    # allow_empty = True # for 404 if objects empty
    h1 = 'xxxxxxxxxxxxxxxxxxxx'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['current_section'] = context['elements'][0].sections[0] # как-то так...
        return self.get_mixin_context(
            context,
            text=f'Cat said - {self.request.GET.get('meow', 'yes')}'
        )

    def get_queryset(self):
        # return self.model.tree
        return self.model.objects.filter(is_active=self.model.Status.ACTIVE).prefetch_related('sections')

class TemplateDetailViewPage(DetailView):

    model = Elements
    slug_url_kwarg = 'element_code'
    # pk_url_kwarg =
    slug_field = 'code'

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model.objects.prefetch_related('sections'),
            code=self.kwargs[self.slug_url_kwarg],
            is_active=self.model.Status.ACTIVE,
        )

class TemplateFormPage(FormView):

    form_class = AddElementForm
    template_name = 'app_catalog/template_form_page.html'
    success_url = reverse_lazy('frontpage')
    extra_context = {
        'text': 'Template form page'
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# class TemplateUpdatePage(UpdateView):
class TemplateCreatePage(LoginRequiredMixin, CreateView):

    # form_class = AddElementForm
    model = Elements
    fields = '__all__'

    template_name = 'app_catalog/template_form_page.html'
    success_url = reverse_lazy('frontpage') # если убрать будет перенаправлен на get_absolute_url
    extra_context = {
        'text': 'Template create page'
    }

    # login_url = 'login' # LoginRequiredMixin

    def form_valid(self, form):
        new_el = form.save(commit=False)
        new_el.author = self.request.user
        return super().form_valid(form)
