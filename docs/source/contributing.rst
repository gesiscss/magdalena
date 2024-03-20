Contributing
============

We use `poetry <https://python-poetry.org>`_ as dependence manager.

Development Environment
-----------------------

With Docker Compose
^^^^^^^^^^^^^^^^^^^

Start the container by running

.. code:: bash

    docker compose up magdalena

and open http://localhost:5000 with your web browser.

Without Docker Compose
^^^^^^^^^^^^^^^^^^^^^^

Install the dependencies by running

.. code:: bash

    poetry install --with dev

and start the server by running

.. code:: bash

    poetry run \
    flask \
    run \
    --host 0.0.0.0 \
    --port 5000 \
    --reload \
    --debug \
    --debugger

and open http://localhost:5000 with your web browser.

Running the Test Collection
----------------------------

We recommend to run the continous integration test in the Docker
container.

Run

.. code:: bash

   docker compose up magdalena

and, in another terminal, run

.. code:: bash

   docker exec magdalena-magdalena-1 -- pytest .

Production Environment
----------------------

With Docker Compose
^^^^^^^^^^^^^^^^^^^

Not supported.

Without Docker Compose
^^^^^^^^^^^^^^^^^^^^^^

Install the dependencies by running

.. code:: bash

    poetry install --with prod

and start the server by running

.. code:: bash

    poetry run \
    gunicorn \
    --workers=2 \
    --bind 0.0.0.0:5000 \
    'wsgi:app'

and open http://localhost:5000 with your web browser.

Documentation Environment
-------------------------

With Docker Compose
^^^^^^^^^^^^^^^^^^^

Start the container by running

.. code:: bash

    docker compose up sphinx

Without Docker Compose
^^^^^^^^^^^^^^^^^^^^^^

Install the dependencies by running

.. code:: bash

    poetry install --only docs

and start the server by running

.. code:: bash

    poetry run \
    sphinx-autobuild \
    --host 0.0.0.0 \
    docs/source \
    docs/build
