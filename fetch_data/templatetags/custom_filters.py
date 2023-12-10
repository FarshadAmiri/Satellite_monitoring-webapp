from django import template

register = template.Library()

@register.filter()
def range(min=1):
    return range(min)