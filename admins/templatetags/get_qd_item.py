from django.template.defaulttags import register


@register.filter
def get_qd_item(item, key):
    print(item, '!!!!!!!!!!!!!!!')
    dict_data = item.__dict__
    print('!!!!', dict_data)
    return dict_data[key]
