import shutil
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from ...packages import update_aarch64, update_x86_64, CACHE_DIR, Archs



class Command(BaseCommand):
    help = 'update packages for branch-compare'
    directory = CACHE_DIR + '/test-bcompare'

    def add_arguments(self, parser):
        parser.add_argument('arch', nargs='?', default="x86_64", help="Architecture : [x86_64] (default) or [arm]", type=str)
        parser.add_argument('--force', action='store_true', help=f"Force all uploads")
        #TODO remove tests
        #parser.add_argument('--test', action='store_true', help=f"Test update but not update DB {self.directory}")

    def _remove_dirs(self, directory: str):
        """Clear download directories"""
        shutil.rmtree(directory + "/" + Archs.x86_64.name, ignore_errors=True)
        shutil.rmtree(directory + "/" + Archs.aarch64.name, ignore_errors=True)

    def handle(self, *args, **options):
        if options['force']:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE compare_lastmodified set date='1999-09-09', status='';")
            self._remove_dirs(CACHE_DIR)
        if options['arch'] == "x86_64":
            update_x86_64(None)
        elif options['arch'] == "arm":
            update_aarch64(None)
