Contributing
============

We use `poetry <https://python-poetry.org>`_ as dependence manager.

Development Environment
-----------------------

.. code:: bash

    poetry install --with dev

.. code:: bash

    poetry run \
    flask \
    run \
    --host 0.0.0.0 \
    --port 5000 \
    --reload \
    --debug \
    --debugger

Production Environment
----------------------

.. code:: bash

    poetry install --with prod

.. code:: bash

    poetry run \
    gunicorn \
    --workers=2 \
    --bind 0.0.0.0:5000 \
    'wsgi:app'

Documentation Environment
-------------------------

.. code:: bash

    poetry install --only docs

Continous Integration Test
--------------------------

We recommend to run the continous integration test in the Docker
container.

Run

.. code:: bash

   docker compose up

and, in another terminal, run

.. code:: bash

   docker exec magdalena-magdalena-1 -- pytest .

User Experience Test
--------------------

We recommend to run the continous integration test in the Docker
container.

Run

.. code:: bash

   docker compose up

and open http://localhost:5000 with your web browser.
