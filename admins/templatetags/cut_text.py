from django.template.defaulttags import register


@register.filter
def cut_text(str):
    if len(str) > 80:
        return str[:80] + '...'
    else:
        return str

