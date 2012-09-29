from django.conf import settings
from django.template.loader import render_to_string
from django.template.base import TemplateDoesNotExist
from django.core.mail import EmailMultiAlternatives

def send(templates_dir, recipient_list, context=None, from_email=settings.DEFAULT_FROM_EMAIL):
    
    if not isinstance(recipient_list, list):
        recipient_list = [recipient_list]
    
    subject = render_to_string("mails/%s/%s" % (templates_dir, "subject.txt"), context)
    
    try:
        body_txt = render_to_string("mails/%s/%s" % (templates_dir, "body.txt"), context)
    except TemplateDoesNotExist,e:
        body_txt = None
        
    try:
        body_html = render_to_string("mails/%s/%s" % (templates_dir, "body.html"), context)
    except TemplateDoesNotExist,e:
        body_html = None
        
    if body_html is None and body_txt is None:
        raise Exception('You must provide a txt or html template: %s' % templates_dir)

   
    msg = EmailMultiAlternatives(subject, body_txt if body_txt is not None else '', from_email, recipient_list)
    if body_html is not None:
        msg.attach_alternative(body_html, "text/html")
        
    return msg.send()