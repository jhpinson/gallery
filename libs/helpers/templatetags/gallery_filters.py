from django import template
import re

register = template.Library()


@register.filter()
def can_edit_field(obj, field): 
    
    print "@TODO can edit field"
    
    return True

@register.filter()
def set_page(url, page):
    
    url = re.sub('&?page=[0-9]+', '', url)
    
    if '?' in url :
        
        if url[-1] == '?':
            url = '%spage=%s' % (url, page)
        else:
            url = "%s&page=%s" % (url, page)
            
    else:
        url = "%s?page=%s" % (url, page)
        
    return url

