from django.template.defaulttags import register


@register.filter
def cut_text(str):
    if len(str) > 100:
        return str[:100] + '...'
    else:
        return str

