from django import template
from django.template.loader import render_to_string
from django.urls import reverse

register = template.Library()

# @register.simple_tag(takes_context=True)
@register.simple_tag()
def get_menu():
    return [
        {
            'link': reverse('frontpage'),
            'title': 'Home',
        },
        {
            'link': reverse('catalog'),
            'title': 'Catalog',
        },
    ]

@register.simple_tag(takes_context=True)
def debug_tpl(context, *args, **kwargs):
    res = {}
    import inspect
    res['inspect_fns'] = inspect.getmembers(args, predicate=inspect.isfunction)
    res['inspect_all'] = inspect.getmembers(args)
    res['inspect_loc'] = inspect.getmembers(kwargs['loc'])
    res['inspect_glob'] = inspect.getmembers(kwargs['glob'])
    return res