import shutil
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from ...packages import Branches, update_aarch64, update_x86_64, CACHE_DIR, Archs



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
        # self.check_datas()
        if options['save']:
            self.bakup()
            exit(0)
        if options['restaure']:
            self.restaure()
            exit(0)
        if options['force']:
            # or DELETE  FROM compare_lastmodified ?
            with connection.cursor() as cursor:
                cursor.execute("UPDATE compare_lastmodified set date='1999-09-09', status='';")
            self._remove_dirs(CACHE_DIR)
        if options['arch'] == "x86_64":
            update_x86_64(None)
        elif options['arch'] == "arm":
            update_aarch64(None)

    def check_datas(self):
        """all datas valides ? we can run a backup"""
        #TODO more tests ???
        from ...models import lastModified

        nb = 0
        with connection.cursor() as cursor:
            for arch in Archs:
                table_name = arch.name
                for abranch in Branches:
                    branch = abranch.name
                    sql = f"""SELECT repo, COUNT({branch})
                        FROM compare_{table_name}
                        WHERE {branch} != ''
                        GROUP BY repo;"""
                    for item in cursor.execute(sql):
                        nb += 1
                        print("   # test ...", table_name, branch, item[0], item[1])
                        if item[1] < 1:
                            return False, f"{arch}/{branch}", item[0]
        if lastModified.objects.filter().count() > nb:
            return False, "lastModified", "error too mutch entries"
        if lastModified.objects.filter(status="ERROR").count():
            return False, "lastModified", "error found in status"
        return True, "", ""


    def bakup(self):
        """ test function for auto backup before all compare db update
        """
        from pathlib import Path
        from django.core import management

        Path(self.backup).parent.mkdir(exist_ok=True)
        ok, err1, err2 = self.check_datas()
        if not ok:
            print("No backup, database is not clear :", err1, err2)
            return

        with open(self.backup, 'w') as fbackup:
            management.call_command("dumpdata", "compare", indent=2, stdout=fbackup)

    def restaure(self):
        from pathlib import Path
        from django.core import management

        if not Path(self.backup).exists():
            print(f"Error: {self.backup} not exists")
            return

        management.call_command('loaddata', self.backup, verbosity=3)
