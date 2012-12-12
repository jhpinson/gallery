from django.utils import simplejson
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.utils.hashcompat import md5_constructor

class JsonSessionMixin(object):
    def encode(self, session_dict):
        "Returns the given session dictionary pickled and encoded as a string."
        pickled = simplejson.dumps(session_dict)
        pickled_md5 = md5_constructor(pickled + settings.SECRET_KEY).hexdigest()
        return pickled + pickled_md5

    def decode(self, session_data):
        pickled, tamper_check = session_data[:-32], session_data[-32:]
        if md5_constructor(pickled + settings.SECRET_KEY).hexdigest() != tamper_check:
            raise SuspiciousOperation("User tampered with session cookie.")
        try:
            
            return simplejson.loads(pickled)
        # Unpickling can cause a variety of exceptions. If something happens,
        # just return an empty dictionary (an empty session).
        except:
            return {}