from django import template


register = template.Library()


@register.filter(name='censor')
def censor(value):
    censor_words = {'хреновый': 'хр*****',
                    'дрянь': 'др***'}
    check = isinstance(value, str)
    if check:
        value = value.lower()
        for i, j in censor_words.items():
            value = value.replace(i, j)
        return value
    else:
        return TypeError
