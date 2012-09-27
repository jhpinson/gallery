from django import template

register = template.Library()


@register.filter()
def can_edit_field(obj, field): 
    
    print "@TODO can edit field"
    
    return True
