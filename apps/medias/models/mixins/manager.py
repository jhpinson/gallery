from middleware.request import get_current_user
from django.db.models.query_utils import Q
                                          
class PermissionManager(object):
    
    def __init__(self, *args, **kwargs):
        
        super(PermissionManager, self).__init__( *args, **kwargs)
        
        self.query.add_q(Q(created_by = get_current_user))