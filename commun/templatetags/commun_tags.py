from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def bold(text, term, autoescape=True):
    return mark_safe(text.replace(term, f'<strong>{ term }</strong>', 1))
