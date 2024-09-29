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