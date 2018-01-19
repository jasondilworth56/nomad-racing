from django import template
from ..models import StaticPage

register = template.Library()

@register.inclusion_tag('nomadmain/static_list.html')
def static_page_list():
    pages = StaticPage.objects.all()
    return {'pages': pages}

@register.inclusion_tag('nomadmain/social_links.html')
def social_links():
    return {}