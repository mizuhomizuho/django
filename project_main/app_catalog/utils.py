class DataMixin:

    extra_context = {}

    def __init__(self):
        if self.h1:
            self.extra_context['h1'] = self.h1
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = {'xxx'}

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = {'yyy'}
        context['cat_selected'] = {}
        context.update(kwargs)
        return context