import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from distutils.core import run_setup
import subprocess


class Command(BaseCommand):
    help = 'Pack module and upload with twine to pypi'

    def add_arguments(self, parser):
        parser.add_argument('module_name', type=str)

    def handle(self, *args, **options):
        module_name = options['module_name']
        self.stdout.write(f'Starting pack module: {module_name}')
        module_dir = os.path.join(settings.BASE_DIR, module_name)
        self.stdout.write(f'Module directory is: {module_dir}')
        tmp_dir = os.path.join(settings.BASE_DIR, 'tmp')
        tmp_module_dir = os.path.join(tmp_dir, module_name)
        self.stdout.write(f'Temp directory is: {tmp_dir}')
        if os.path.exists(tmp_dir):
            self.stdout.write('Clean temp directory...')
            shutil.rmtree(tmp_dir)
        self.stdout.write('Starting copy files to temp directory...')
        os.makedirs(tmp_dir, exist_ok=True)
        shutil.copytree(module_dir, tmp_module_dir)
        shutil.copyfile(os.path.join(module_dir, 'setup.py'), os.path.join(tmp_dir, 'setup.py'))
        shutil.copyfile(os.path.join(module_dir, 'MANIFEST.in'), os.path.join(tmp_dir, 'MANIFEST.in'))
        os.chdir(tmp_dir)
        run_setup(os.path.join(tmp_dir, 'setup.py'), script_args=['sdist', 'bdist_wheel'])
        subprocess.call(["twine", "upload", "dist/*"], cwd=tmp_dir)
        self.stdout.write(self.style.SUCCESS('Done'))
