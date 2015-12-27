.. _birdie_stage0:

=======
Stage 0
=======

In the previous step, you setup your development environment and its
requirements, which includes a Python interpreter, packaging software, and
Pyramid. Next you will create a project from one of Pyramid's scaffolds.

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
