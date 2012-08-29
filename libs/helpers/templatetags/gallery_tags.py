from django import template

register = template.Library()


@register.simple_tag()
def image_thumbnail(value, size):
    
    data = getattr(value, 'thumbnail_%s' % size)
    
    if data['exists'] is True:
        return '<img src="%(url)s" width="%(width)s" height="%(height)s">' %  data
    
    else:
        return '<img class="thumbnail-pending" data-generate="%(url)s" src="#" width="%(width)s" >' %  data
    
    