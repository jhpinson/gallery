from django import template

register = template.Library()


@register.simple_tag()
def image_thumbnail(value, size):
    
    data = getattr(value, 'thumbnail_%s' % size)()
    
    data = dict(data, pk=value.pk)
    
    if data['exists'] is True:
        return '<img data-media="%(pk)s" src="%(url)s" width="%(width)s" height="%(height)s">' %  data
    
    else:
        return '<img class="thumbnail-pending" data-media="%(pk)s" data-generate="%(url)s" src="#" width="%(width)s" height="%(height)s">' %  data
    
    