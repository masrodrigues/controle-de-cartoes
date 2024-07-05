from django import template

register = template.Library()

@register.filter
def email_username(email):
    return email.split('@')[0]
