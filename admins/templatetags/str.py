from django.template.defaulttags import register


@register.filter
def to_string(val):
    return str(val)