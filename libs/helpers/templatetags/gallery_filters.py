from django import template
import re, urlparse
from django.template.defaultfilters import stringfilter
from django.contrib.sites.models import Site

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

@register.filter
@stringfilter
def css_class(value):
    value = value.lower().strip()
    return re.sub(r'\s+', '-', value)


@register.filter
@stringfilter
def make_absolute_url(value):
    p = urlparse.urlparse(value)
    if p.netloc == '':
        domain = Site.objects.get_current().domain
        return urlparse.urljoin("http://%s/" % domain, value)
    else:
        return value