.. _birdie_stage1:

=======
Stage 1
=======

In the previous step, created a default project from the Pyramid ``alchemy``
scaffold. Next you will add a database model, create two views, and use
Chameleon for your templates.


Add a database model
--------------------

We can delete the SQLite database that we initialized in the previous step.

.. code-block:: bash

    $ rm MyBirdie.sqlite

Next let's create a new database model. Open ``mybirdie/models.py`` and edit it
as follows.

.. literalinclude:: src/stage1/mybirdie/models.py
    :language: python
    :linenos:
    :emphasize-lines: 3-5,21-22,24-26

We need to modify the database initialization script, too. Edit
``mybirdie/scripts/initializedb.py`` as follows.

.. literalinclude:: src/stage1/mybirdie/scripts/initializedb.py
    :language: python
    :linenos:
    :lineno-start: 14
    :lines: 14-
    :emphasize-lines: 3,26

Now let's initialize the database by running the script from the command line.

.. code-block:: bash

    $ $VENV/bin/initialize_MyBirdie_db development.ini


Create views
------------

Now let's make two views. The first one will be for displaying all the chirps,
and the second will be for posting a new chirp. Templates use chameleon.


Copied from Stage 0 - OK to delete
----------------------------------

At the command line, make sure your current working directory is ``birdie``.
Then issue the following command.

.. code-block:: bash

    $ $VENV/bin/pcreate -s alchemy MyBirdie

A new project is created at ``birdie/MyBirdie``. The Pyramid scaffold
``alchemy`` generated a directory containing files that are commonly used in a
Pyramid project.

Let's verify that the default project works. Issue the following commands.

.. code-block:: bash

    $ cd MyBirdie
    # install the project and its dependencies for development
    $ $VENV/bin/python setup.py develop
    # initialize the SQLite database for the default project
    $ $VENV/bin/initialize_MyBirdie_db development.ini
    # run the app
    $ $VENV/bin/pserve development.ini --reload

Visit http://0.0.0.0:6543 in a web browser to view the running ``MyBirdie``
application.

In our next step, we'll start customizing the default project.
