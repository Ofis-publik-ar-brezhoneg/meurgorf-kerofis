from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def bold(text, term, autoescape=True):
    return mark_safe(text.replace(term, f'<strong>{ term }</strong>', 1))


@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)
