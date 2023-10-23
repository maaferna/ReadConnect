from django import template

register = template.Library()

@register.filter
def get_nested_dict_value(dictionary, key):
    try:
        keys = key.split('.')
        value = dictionary
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        return None
