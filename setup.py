from setuptools import setup, find_packages

import sys

if sys.version_info.major < 3:
    print('Please install with python version 3')
    sys.exit(1)

from distutils.core import Command
from distutils.core import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        if len(self.pytest_args) == 0:
            self.pytest_args = ['--cov=buildstrap', '--cov-report=term-missing']
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class dist_clean(Command):
    description = 'Clean the repository from all buildout stuff'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


    def run(self):
        import shutil, os
        from glob import glob
        path = os.path.split(__file__)[0]
        shutil.rmtree(os.path.join(path, 'var'), ignore_errors=True)
        shutil.rmtree(os.path.join(path, 'bin'), ignore_errors=True)
        shutil.rmtree(os.path.join(path, '.tox'), ignore_errors=True)
        for fname in glob('*.egg-info'):
            shutil.rmtree(os.path.join(path, fname), ignore_errors=True)
        shutil.rmtree(os.path.join(path, '.eggs'), ignore_errors=True)
        shutil.rmtree(os.path.join(path, 'build'), ignore_errors=True)
        shutil.rmtree(os.path.join(path, 'dist'), ignore_errors=True)
        shutil.rmtree(os.path.join(path, '.installed.cfg'), ignore_errors=True)
        print("Repository is now clean!")

version = open('VERSION', 'r').read().strip()

setup(name='buildstrap',
      version=version,
      description='Tool for managing remote repositories from your git CLI!',
      classifiers=[
          # 'Development Status :: 2 - Pre-Alpha',
          # 'Development Status :: 3 - Alpha',
          'Development Status :: 4 - Beta',
          # 'Development Status :: 5 - Production/Stable',
          # 'Development Status :: 6 - Mature',
          # 'Development Status :: 7 - Inactive',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Framework :: Buildout',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: Freely Distributable',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Utilities',
      ],
      keywords='git',
      url='https://github.com/guyzmo/buildstrap',
      author='Bernard `Guyzmo` Pratz',
      author_email='guyzmo+buildstrap+pub@m0g.net',
      setup_requires=[
          'setuptools-markdown'
      ],
      long_description_markdown_filename='README.md',
      include_package_data = True,
      install_requires=[
            'docopt',
            'zc.buildout',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      buildstrap = buildstrap.buildstrap:run
      """,
      license='WTFPL',
      packages=find_packages(exclude=['tests']),
      cmdclass={
          'test': PyTest,
          'dist_clean': dist_clean
      },
      tests_require=[
          'pytest',
          'pytest-cov',
          'pytest-sugar',
          'pytest-catchlog',
          'pytest-datadir-ng',
      ],
      zip_safe=False
      )
