import shutil
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from ...packages import update_aarch64, update_x86_64, CACHE_DIR, Archs



class Command(BaseCommand):
    help = 'update packages for branch-compare'
    directory = CACHE_DIR + '/test-bcompare'
    backup = "compare/backup/compare_backup.json"

    def add_arguments(self, parser):
        parser.add_argument('arch', nargs='?', default="x86_64", help="Architecture : [x86_64] (default) or [arm]", type=str)
        parser.add_argument('--force', action='store_true', help=f"Force all uploads")
        parser.add_argument('--save', action='store_true', help=f"Save in {self.backup}")
        parser.add_argument('--restaure', action='store_true', help=f"Restaure from {self.backup}")
        #TODO remove tests
        #parser.add_argument('--test', action='store_true', help=f"Test update but not update DB {self.directory}")

    def _remove_dirs(self, directory: str):
        """Clear download directories"""
        shutil.rmtree(directory + "/" + Archs.x86_64.name, ignore_errors=True)
        shutil.rmtree(directory + "/" + Archs.aarch64.name, ignore_errors=True)

    def handle(self, *args, **options):
        if options['save']:
            self.bakup()
            exit(0)
        if options['restaure']:
            self.restaure()
            exit(0)
        if options['force']:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE compare_lastmodified set date='1999-09-09', status='';")
            self._remove_dirs(CACHE_DIR)
        if options['arch'] == "x86_64":
            update_x86_64(None)
        elif options['arch'] == "arm":
            update_aarch64(None)

    def bakup(self):
        """ test function for auto backup before all compare db update
        """
        from pathlib import Path
        from django.core import management
        from ...models import lastModified

        Path(self.backup).parent.mkdir(exist_ok=True)
        # if lastModified.objects.count() != lastModified.objects.filter(status="ok" or '' and date > 2000):
        if lastModified.objects.filter(status="ERROR").count():     # good condition ?
            print("No backup, database is not clear")
            return

        #management.call_command("flush", verbosity=0, interactive=False)
        with open(self.backup, 'w') as fbackup:
            management.call_command("dumpdata", "compare", indent=2, stdout=fbackup)

    def restaure(self):
        from pathlib import Path
        from django.core import management

        if not Path(self.backup).exists():
            print(f"Error: {self.backup} not exists")
            return

        management.call_command('loaddata', self.backup, verbosity=3)
