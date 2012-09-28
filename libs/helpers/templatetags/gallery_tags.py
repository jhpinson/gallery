from django import template
import re
register = template.Library()


@register.simple_tag()
def image_thumbnail(value, size):
    
    data = getattr(value, 'thumbnail_%s' % size)()
    
    data = dict(data, pk=value.pk)
    
    if data['exists'] is True:
        return '<img data-media="%(pk)s" src="%(url)s" width="%(width)s" height="%(height)s">' %  data
    
    else:
        return '<img class="thumbnail-pending" data-media="%(pk)s" data-generate="%(url)s" src="#" width="%(width)s" height="%(height)s">' %  data
    

@register.simple_tag()
def set_qs(url, param, value):
    
    url = re.sub('&?'+param+'=[0-9]+', '', url)
    
    if '?' in url :
        
        if url[-1] == '?':
            url = '%s%s=%s' % (url, param, value)
        else:
            url = "%s&%s=%s" % (url, param, value)
            
    else:
        url = "%s?%s=%s" % (url, param, value)
        
    return url