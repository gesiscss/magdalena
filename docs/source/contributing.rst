Contributing
============

We use `poetry <https://python-poetry.org>`_ as dependence manager.

Development Environment
-----------------------

.. code:: bash

    poetry install --with dev

Production Environment
----------------------

.. code:: bash

    poetry install --with prod

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
