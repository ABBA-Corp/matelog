from django.template.defaulttags import register


@register.filter
def list_item(list, i):
    index = i - 1
    print(list)
    return list[index]
