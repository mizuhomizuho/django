from django.shortcuts import render, get_object_or_404
from app_catalog.models import Sections, Elements

class AppCatalogView:

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
        items = Elements.objects.filter(sections=section_el).prefetch_related('sections') # select_related - для OTM и OTO
        # raise Http404()
        # return redirect('section', 'cat1/cat2', 'cat3', permanent=True)
        return render(request, 'app_catalog/section.html', context={
            'tree': Sections.tree.get()['tree'],
            'section': section_el,
            'items': items,
        })