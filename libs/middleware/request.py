import threading
_thread_locals = threading.local()

class ThreadRequestMiddleware(object):
   
    def process_request(self, request):
        setattr(_thread_locals, 'request' ,request)
        
        
        

def get_current_user():
    
    if getattr(_thread_locals, 'user', None) is not None:
        return getattr(_thread_locals, 'user', None)
    
    request = getattr(_thread_locals, 'request', None)
    return None if request.user.is_anonymous() else request.user
        
    
    
def set_current_user(user):
    setattr(_thread_locals, 'user', user)
