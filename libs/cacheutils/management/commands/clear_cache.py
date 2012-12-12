#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from optparse import make_option
from cacheutils.manager import manager

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (make_option('-a', '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Flush all caches'),
            make_option('-l', '--list',
            action='store_true',
            dest='list',
            default=False,
            help='List all caches'),
            make_option('-e', '--exclude',
            action='append',
            dest='exclude',
            default=[],
            help='Exclude emply --all'),)
    
    def handle(self, *args, **options):
        if len(options['exclude']) > 0:
            manager.clear_all(exclude=options['exclude'])
        elif options['all']:
            manager.clear_all()
        elif options['list']:
            manager.list()
        else:
            for cache_name in args:
                manager.clear(cache_name)


