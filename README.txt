TAASKS
======

The taasks are really important so be sure to read the text below before
starting to work on it. Seriously.

Installation and preparation
============================

    $ mkdir -p /project/parent/folders

    $ cd /project/parent/folders

    $ git clone ssh://dev/code/taasks.git

    $ cd taasks

    $ virtualenv .
      The project is being developed using python 2.6 though might work with
      other versions as well

Install all the dependencies (including django):
    $ bin/python setup.py develop

(Temporary) Until South catches up with Django 1.2 apply a patch:
    $ ./temp/south-patch

    $ cd taasks

Create tables for the third party packages:
    $ ../bin/python manage.py syncdb --noinput
      This also loads initial_data.xml. This data contains things like groups
      and group-permission relationships we rely on. However, the
      group-permission relationships are based on foreign keys which can change
      any time so this is a problem we need to address at some point.
      We prefer xml over json because it does not throw NotJSONSerializable
      errors. If you hate xml'ing, use
        $ ../bin/python manage.py dumpdata --format=xml --indent=2 > initial_data.xml
      to generate the current DB state and remove what's not needed.

Create the database schema using the database migrations (south):
    $ ../bin/python manage.py migrate
      Until South catches up with Django 1.2 please issue this command several
      times until all the migrations are finished. Ignore the errors.

(Optional) If you need an admin user you can create it now using
    $ ../bin/python manage.py createsuperuser
      This will NOT work before the database is migrated

(Optional) If you don't want to enter ../bin/python manage.py (or whatever)
all the time you can do
    $ echo "../bin/python manage.py \"\$@\"" > manage
    $ chmod +x manage
so later you can just
    $ ./manage test tasks
instead of
    $ ../bin/python manage.py test tasks

Development guidelines
======================

- Respect other people' work and use 3rd party projects

- Don't forget to
    $ ../bin/python manage.py test
      While we are working with unstable some 3rd party packages won't pass
      tests. But we should test our packages nevertheless.


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
