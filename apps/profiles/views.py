from helpers.rest.views import BackboneView
from .models import Profile

class RestProfileView(BackboneView):
    model = Profile
    url_root = "rest/users"
    
    