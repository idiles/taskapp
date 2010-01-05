TAASKS
======

The taasks are really important so be sure to read the text below before
starting to work on it. Seriously.

Installation and preparation
============================

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


Development guidelines
======================

- Respect other people work and use third party projects
- Don't forget to

    $ ../bin/python manage.py test


Third party projects in use
===========================

south
-----

http://south.aeracode.org

We want to have a stable database model, track database changes in a
_decentralized_ way preserving our test data regardless of the changes.

We think that south is currently the best-of-breed.


Third party projects to consider
================================

django_compressor
-----------------

http://github.com/mintchaos/django_compressor

The CSS and JS has to be compressed to be served in production. This tool should
do it. If we could contribute a filter that would replace

    {{ MEDIA_URL }}
    with
    /static     (or whatever)
    
    and

    {% url my_named_url some_id='my_variable' %}
    with
    '/my/named/url/' + my_variable + '/included/as.string'

we could not desire anything more.

CleverCSS
---------

http://github.com/dziegler/clevercss

This one's a companion for django_compressor. Maybe worth a try if the css
becomes complex enough.
