from django import template

register = template.Library()

@register.filter
def get_tags(value):
    if isinstance(value, list):
        return ", ".join([x.name for x in value])
    else:
        return value
