TAASKS
======

The taasks are really important so be sure to read the text below before
starting to work on it. Seriously.

Installation
============

    $ mkdir -p /an/empty/folder

    $ cd /an/empty/folder

    $ virtualenv .
      The project is being developed using python 2.6 though might work with
      other versions as well

    $ git pull ssh://dev/code/taasks.git taasks

This will be removed as soon as Django officially releases 1.2:

    $ bin/easy_install http://code.djangoproject.com/svn/django/trunk/

This installs all the dependencies:

    $ bin/python setup.py develop

    $ cd taasks

Create tables for the third party packages:

    $ ../bin/python manage.py syncdb

Create the database schema using the database migrations (south):

    $ ../bin/python manage.py migrate


Third party projects in use
===========================

south
-----

http://south.aeracode.org

We want to have a stable database model, track database changes in a
decentralized way preserving our test data regardless of the changes.

We think that south is currently the best-of-breed.
