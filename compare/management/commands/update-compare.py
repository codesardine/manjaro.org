from pathlib import Path
import shutil
from django.core.management.base import BaseCommand, CommandError
from ...packages import update_aarch64, update_x86_64, CACHE_DIR, Archs


class Command(BaseCommand):
    help = 'update packages for branch-compare'
    directory = CACHE_DIR + '/test-bcompare'

    def add_arguments(self, parser):
        parser.add_argument('arch', nargs='?', default="x86_64", help="Architecture : [x86_64] (default) or [arm]", type=str)
        parser.add_argument('--force', action='store_true', help=f"Remove downloads in {CACHE_DIR}")
        parser.add_argument('--test', action='store_true', help=f"Test update but not update DB {self.directory}")

    def _remove_dirs(self, directory: str):
        """Clear download directories"""
        shutil.rmtree(directory + "/" + Archs.x86_64.name, ignore_errors=True)
        shutil.rmtree(directory + "/" + Archs.aarch64.name, ignore_errors=True)

    def handle(self, *args, **options):
        if options['force']:
            self._remove_dirs(CACHE_DIR)
        if options['test']:
            self._remove_dirs(self.directory)
            # Path(self.directory).mkdir(exist_ok=True)
        if options['arch'] == "x86_64":
            update_x86_64(self.directory if options['test'] else None)
        elif options['arch'] == "arm":
            update_aarch64(self.directory if options['test'] else None)
        if options['test']:
            self._remove_dirs(self.directory)
