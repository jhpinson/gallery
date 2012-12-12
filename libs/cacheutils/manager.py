import redis

class Manager(object):
    
    _registry = {}
    
    def register(self, name, engine, settings):
        
        self._registry[name] = {
            "engine" : engine,
            "settings" : settings
        }
    def update_settings(self, name, settings):
        if self._registry.get(name,None) is None:
            print "Can't update settings for cache name %s : not registred" % name
        else:
            cache = self._registry[name]
            cache['settings'].update(settings)
            self._registry[name] = cache

    def clear(self, name):
        if self._registry.get(name,None) is None:
            print "Can't clear cache name %s : not registred" % name
        else:
            cache = self._registry.get(name) 
            if cache['engine'] == 'redis':
                print "Clearing cache %s" % name
                try:
                    redis.Redis(**cache['settings']).execute_command('FLUSHDB')
                    print "Success"
                except Exception, e:
                    print "Error ", e

            else:
                print "I don't know how to deal with %s engine, could you teach me for next time ?" % cache['engine']
       
    def clear_all(self, exclude=[]):
        for name in self._registry.keys():
            if name in exclude:
                continue
            self.clear(name)

    def list(self):
        for name in self._registry.keys():
            if self._registry[name]['engine'] == 'redis':
                print "%-20s %-10s" % (name, self._registry[name]['engine']), "%(host)-18s:%(port)s db:%(db)s" % self._registry[name]['settings']
            else:
                print name, self._registry[name]['engine']
manager = Manager()
