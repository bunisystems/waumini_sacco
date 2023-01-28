from tokenize import group
from django import template
from django.contrib.auth.models import Group
from django.core.cache import cache

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    # Store the results of a query in the cache
    group = Group.objects.get(name=group_name)
    cache.set('group', group, 60 * 60)
    # Retrieve the results of a query from the cache
    g = cache.get('group')
    return True if g in user.groups.all() else False