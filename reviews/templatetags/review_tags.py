from django import template

register = template.Library()


def dictionary_get(value, arg):
    return value.get(arg)


register.filter('dictionary_get', dictionary_get)
