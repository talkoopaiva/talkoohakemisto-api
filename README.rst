Talkoohakemisto API
===================

Requirements
------------

- Python 2.7
- `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/>`_
- `autoenv <https://github.com/kennethreitz/autoenv>`_


Development
-----------

Follow the instructions below to set up the development environment.

1. Create a new virtualenv::

    $ mkvirtualenv talkoohakemisto-api

2. Make the virtualenv activate automagically when traversing inside the
   project directory::

    $ echo -e "use_env talkoohakemisto-api\n" > .env

3. Create databases for development and testing::

    $ createdb talkoohakemisto
    $ createdb talkoohakemisto_test

4. Create database tables::

    $ alembic upgrade head

5. Finally, start the development server::

    $ python manage.py runserver


Testing
-------

You can run the tests with `py.test <http://pytest.org>`_::

    $ py.test
