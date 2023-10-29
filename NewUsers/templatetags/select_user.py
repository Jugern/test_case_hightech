from django import template
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
register = template.Library()


@register.inclusion_tag('listUsers.html')
def setUsers(auth):
    Users = get_user_model()
    spisok = Users.objects.all()
    return {'spisok': spisok,
            'auth': auth,
            }


@register.filter
def setURL(url):
    return str(url)

