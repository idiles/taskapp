from setuptools import setup, find_packages
import sys, os

version = '0.1a'

setup(name='Taasks',
    version=version,
    description="Task and project management system",
    long_description=open('README.txt').read(),
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Idiles',
    author_email='hello@idiles.com',
    url='www.idiles.com',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests']),
    include_package_data=True,
    namespace_packages=[],
    zip_safe=False,
    install_requires=[
        'Django>1.1.1',
        'South>=0.6.2',
    ],
    dependency_links=[
        'http://media.djangoproject.com/releases/1.2/Django-1.2-alpha-1.tar.gz'
    ],
    entry_points="""
    """,
    )
