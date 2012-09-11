import threading
_thread_locals = threading.local()

class ThreadRequestMiddleware(object):
   
    def process_request(self, request):
        setattr(_thread_locals, 'request' ,request)
        
        
        

def get_current_user():
    
    try:
        request = getattr(_thread_locals, 'request', None)
        return None if request.user.is_anonymous() else request.user
        
    except:
        return None