from django import template
import re
from django.template.base import Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str
register = template.Library()


@register.simple_tag()
def image_thumbnail(value, size):
    
    data = getattr(value, 'thumbnail_%s' % size)()
    
    data = dict(data, pk=value.pk)
    
    if data['exists'] is True:
        
        _data = {'id' : "media-%(pk)s" % data,
                 'width' : data['width'],
                 'height' : data['height'],
                 'data-tags' : 'data-media="%(pk)s"' % data,
                 'class' : '',
                 'src' : data['url']
                 }
        
        return '<img id="media-%(pk)s" data-media="%(pk)s" src="%(url)s" width="%(width)s" height="%(height)s">' %  data
    
    else:
        
        _data = {'id' : "media-%(pk)s" % data,
                 'width' : data['width'],
                 'height' : data['height'],
                 'data-tags' : 'data-media="%(pk)s" data-generate="%(url)s"' % data,
                 'class' : 'thumbnail-pending',
                 'src' : '#'
                 }
        
        return '<img class="thumbnail-pending" id="media-%(pk)s" data-media="%(pk)s" data-generate="%(url)s" src="#" width="%(width)s" height="%(height)s">' %  data
    



kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')


class ThumbNode(Node):
    
    nodelist_empty = NodeList()
    
    child_nodelists = ('nodelist_file', 'nodelist_empty')
    error_msg = ('Syntax error. Expected: ``image media size '
                 '[key1=val1 key2=val2...] as var``')

    def __init__(self, parser, token):
        bits = token.split_contents()
        if len(bits) < 5 or bits[-2] != 'as':
            raise TemplateSyntaxError(self.error_msg)
        
        self.media = parser.compile_filter(bits[1])
        self.size = parser.compile_filter(bits[2])
        
        self.as_var = bits[-1]
        self.nodelist_file = parser.parse(('empty', 'endthumb',))
        if parser.next_token().contents == 'empty':
            self.nodelist_empty = parser.parse(('endthumb',))
            parser.delete_first_token()

    def render(self, context):
        media = self.media.resolve(context)
        size = self.size.resolve(context)
        
        if media:
            
            
            data = getattr(media, 'thumbnail_%s' % size)()
        
            _data = {'id' : "media-%(pk)s" % data,
                     'width' : data['width'],
                     'height' : data['height'],
                     'src' : data['url']
                     }
            
           
            
            context.push()
            context[self.as_var] = _data
            output = self.nodelist_file.render(context)
            context.pop()
            return output
            
        else:
            return self.nodelist_empty.render(context)
        
        

    def __repr__(self):
        return "<ThumbNode>"

    def __iter__(self):
        for node in self.nodelist_file:
            yield node
        for node in self.nodelist_empty:
            yield node


@register.tag
def thumb(parser, token):
    return ThumbNode(parser, token)

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