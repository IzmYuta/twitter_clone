from django import template

register = template.Library()


@register.filter(name="in_group")
def in_group(user, group):
    for person in group:
        if person.followed == user:
            return True
            break
    return False
