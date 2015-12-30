.. _birdie_stage1:

=======
Stage 1
=======

In the previous step, created a default project from the Pyramid ``alchemy``
scaffold. Next you will add a database model, create a route and two views, and
use Chameleon for your templates.


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


Create route and views
----------------------

Let's configure our app. Open and edit ``mybirdie/__init__.py`` as follows.



Now let's make two views. The first one will be for displaying all the chirps,
and the second will be for posting a new chirp.

Open ``mybirdie/views.py`` and completely replace its contents with the
following.



In the first few lines, we import classes we need in the views.

The view ``birdie_view`` accepts a Pyramid ``request`` object. It initializes a
database session, then queries the database for chirps where the author is
"anonymous", sorts them in order of most recent first, limiting to 30 records.
The result set is returned in a dict with the key ``chirps``, along with a few
other items.

Next for creating a chirp, we use the view ``birdie_post``, which also accepts
a Pyramid ``request`` object and initializes a database session. It then gets
the POST parameter ``chirp``, assigning its value to the variable of the same
name. We assign values for both ``author`` and ``timestamp``, and create a new
``Chirp`` object from the three variables. Then the new chirp object is added
to the database as a new record. The rest of the view is exactly the same as
our previous view, returning the 30 most recent chirps.


Create templates using Chameleon
--------------------------------

Next we need to render the response through a template that uses Chameleon. You
can rename the default template file from the scaffold from
``mybirdie/templates/mytemplate.pt`` to ``mybirdie/templates/birdie.pt``, then
edit it as indicated.

Run the app
-----------

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
