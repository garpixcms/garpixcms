from setuptools import setup, find_packages
from os import path

here = path.join(path.abspath(path.dirname(__file__)), 'garpixcms')

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='garpixcms',
    version='3.53.0-rc2',
    description='',
    long_description=long_description,
    url='https://github.com/garpixcms/garpixcms',
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
        'Django >= 3.1, < 4',
        'garpix_utils == 1.8.0',
        'garpix_page == 2.42.0-rc2',
        'garpix_menu == 1.13.0',
        'eqator == 2.6.0',
        'garpix_auth == 2.3.0',
        'garpix_notify == 5.13.6',
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
        'django-tabbed-admin >= 1.0.4',
    ],
)
