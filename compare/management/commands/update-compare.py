import shutil
from django.core.management.base import BaseCommand
from django.db import connection
from ...packages import update_aarch64, update_x86_64, CACHE_DIR
from ...models import Archs, Branches, ReportPackages



class Command(BaseCommand):
    help = 'update packages for branch-compare'
    directory = f'{CACHE_DIR}/test-bcompare'
    backup_path = "compare/backup/compare_backup.json"

    def add_arguments(self, parser):
        parser.add_argument('arch', nargs='?', default=f"{Archs.x86_64.name}", help=f"Architecture : [{Archs.x86_64.name}] (default) or [arm]", type=str)
        parser.add_argument('--force', action='store_true', help=f"Force all uploads")
        parser.add_argument('--save', action='store_true', help=f"Save in {self.backup_path}")
        parser.add_argument('--restore', action='store_true', help=f"Restore from {self.backup_path}")
        #TODO remove tests
        #parser.add_argument('--test', action='store_true', help=f"Test update but not update DB {self.directory}")

    def _remove_dirs(self, directory: str):
        """Clear download directories"""
        shutil.rmtree(f'{directory}/{Archs.x86_64.name}', ignore_errors=True)
        shutil.rmtree(f'{directory}/{Archs.aarch64.name}', ignore_errors=True)

    def handle(self, *args, **options):
        """Run command manage.py update-compare"""

        self.make_report_packages()

        # self.check_datas()
        if options['save']:
            self._backup()
            exit(0)
        if options['restore']:
            self.restore()
            exit(0)
        try:
            if options['force']:
                # or DELETE  FROM compare_lastmodified ?
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE compare_lastmodified set date='1999-09-09', status='';")
                self._remove_dirs(CACHE_DIR)
            if options['arch'] == "x86_64":
                update_x86_64(None)
            elif options['arch'] == "arm":
                update_aarch64(None)
        finally:
            self.make_report_packages()

    def check_datas(self):
        """ is all data valid? we can run a backup"""
        #TODO more tests ???
        from ...models import lastModified

        nb = 0
        with connection.cursor() as cursor:
            for arch in Archs:
                for abranch in Branches:
                    branch = abranch.name
                    sql = f"""SELECT repo, COUNT({branch})
                        FROM compare_packagemodel
                        WHERE {branch} != '' AND architecture="{arch.value}"
                        GROUP BY repo;"""
                    for item in cursor.execute(sql):
                        nb += 1
                        print("   # test ...", arch.name, branch, item[0], item[1])
                        if item[1] < 1:
                            return False, f"{arch}/{branch}", item[0]
        if lastModified.objects.filter().count() > nb:
            return False, "lastModified", "error too many entries"
        if lastModified.objects.filter(status="ERROR").count():
            return False, "lastModified", "status error found"
        return True, "", ""

    def make_report_packages(self):
        report = ReportPackages()
        report.request()

        for arch in Archs:
            print(f"\n{'-' * (16+1+9+9+9)}")
            print(f"{arch.name:16} {'stable':>9}{'testing':>9}{'unstable':>9}")
            for item in report.items[arch.name]:
                print(f'{item.repo:16} {item.stables:>9}{item.testings:>9}{item.unstables:>9}')
            totals = report.get_total(arch)
            print(f'{" ":16} {totals.stables:>9}{totals.testings:>9}{totals.unstables:>9}')
            print(f"{'-' * (16+1+9+9+9)}")

    def _backup(self):
        """ test function for auto backup before all compare db update
        """
        from pathlib import Path
        from django.core import management

        Path(self.backup_path).parent.mkdir(exist_ok=True)
        ok, err1, err2 = self.check_datas()
        if not ok:
            print("No backup, database is not clear :", err1, err2)
            return

        with open(self.backup_path, 'w') as fbackup:
            management.call_command("dumpdata", "compare", indent=2, stdout=fbackup)

    def restore(self):
        from pathlib import Path
        from django.core import management

        if not Path(self.backup_path).exists():
            print(f"Error: {self.backup_path} not exists")
            return

        management.call_command('loaddata', self.backup_path, verbosity=3)
