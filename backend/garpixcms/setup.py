from setuptools import setup, find_packages
from os import path

here = path.join(path.abspath(path.dirname(__file__)), 'garpixcms')

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='garpixcms',
    version='4.6.0-rc34',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/garpixcms/garpixcms',
    project_urls={
        'Documentation': 'https://docs.garpixcms.ru/',
        'GitHub': 'https://github.com/garpixcms/garpixcms/',
        'Changelog': 'https://github.com/garpixcms/garpixcms/blob/master/CHANGELOG.md/',
    },
    author='Garpix LTD',
    author_email='info@garpix.com',
    license='MIT',
    packages=find_packages(exclude=['testproject', 'testproject.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django >= 3.1, < 5',
        'garpix_utils >= 1.10, < 2',
        'garpix_page >= 2.49.0-rc5, < 3',
        'garpix_menu == 1.17.1',
        'eqator >= 2.7, < 3',
        'garpix_auth == 2.3.0',
        'garpix_notify == 5.17.0-rc1',
        'garpix_user == 3.10.0-rc24',
        'garpix_package == 2.0.1',
        'psycopg2-binary >= 2.8.6',
        'uwsgi >= 2.0.19.1',
        'environs >= 9.3.2',
        'django-ckeditor == 6.3.0',
        'djangorestframework >= 3.12.4',
        'django-cors-headers >= 3.7.0, <= 3.13.0',
        'drf-spectacular >= 0.18.2',
        'sentry-sdk >= 1.5.2',
        'pre-commit >= 2.17.0',
    ],
)
