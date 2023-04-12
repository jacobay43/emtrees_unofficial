from django import template

register = template.Library()

@register.filter
def to_hyphen(value):
    return value.replace(' ','-')