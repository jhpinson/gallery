from django.core.management.base import NoArgsCommand
from django.conf import settings
import sys, os, signal

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        try:
            pid_file = settings.SITE_ROOT / 'pid/uwsgi.pid'
            pid = int(open(pid_file).read().strip())
        except IOError:
            print "Uwsgi pid file is missing"
            sys.exit(1)
        os.kill (pid, signal.SIGHUP)
        print "uWSGI reloaded"
