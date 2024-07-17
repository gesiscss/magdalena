.. SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
.. SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
..
.. SPDX-License-Identifier: AGPL-3.0-or-later

Contributing
============

Requirements
------------

-  Git
-  Docker
-  Docker Compose
-  `Poetry <https://python-poetry.org/>`_

Configuration
-------------

You need to define a couple of local domain names.

Virtual Private Server (VPS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are using a server provided by IT for development, for example
``svk-my-server.gesis.intra`` with IP ``10.22.15.xxx``, add

::

   # Used by GESIS Keycloak for Development
   #
   # https://git.gesis.org/rse/keycloak
   10.22.15.xxx       methodshub.gesis
   10.22.15.xxx       keycloak.gesis

to the file ``/etc/hosts`` on GNU/Linux laptop or to the file
``C:\Windows\System32\drivers\etc\hosts`` on your Windows laptop.

Windows and Windows Subsystem for Linux (WSL2)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add

::

   # Used by GESIS Keycloak for Development
   #
   # https://git.gesis.org/rse/keycloak
   127.0.0.1       methodshub.gesis
   127.0.0.1       keycloak.gesis

to the file ``C:\Windows\System32\drivers\etc\hosts``.

GNU/Linux
^^^^^^^^^

Add

::

   # Used by GESIS Keycloak for Development
   #
   # https://git.gesis.org/rse/keycloak
   127.0.0.1       methodshub.gesis
   127.0.0.1       keycloak.gesis

to the file ``/etc/hosts``.

Quick Start
-----------

The faster way to start is with `Docker
Compose <https://docs.docker.com/compose/>`__ by running

.. code:: bash

   docker compose up -d reverse-proxy && docker compose logs -f reverse-proxy magdalena-web magdalena-worker

The frontend will be available at http://methodshub.gesis. To login, use the credential below:

+------------+--------------+------------+-----------+---------------------------------------------------------------------------------------------------+--------------------------------+
| Realm      | Username     | Password   | Roles     | Notes                                                                                             |                                |
+============+==============+============+===========+===================================================================================================+================================+
| ``master`` | ``admin``    | ``123456`` |           |                                                                                                   | Only for http://keycloak.gesis |
+------------+--------------+------------+-----------+---------------------------------------------------------------------------------------------------+--------------------------------+
| ``gesis``  | ``ano``      | ``123``    |           | `A. N. Other <https://en.wikipedia.org/wiki/A._N._Other>`__ is a gender neutral placeholder name. |                                |
+------------+--------------+------------+-----------+---------------------------------------------------------------------------------------------------+--------------------------------+
| ``gesis``  | ``jane.doe`` | ``123``    |           |                                                                                                   |                                |
+------------+--------------+------------+-----------+---------------------------------------------------------------------------------------------------+--------------------------------+
| ``gesis``  | ``john.doe`` | ``123``    |           |                                                                                                   |                                |
+------------+--------------+------------+-----------+---------------------------------------------------------------------------------------------------+--------------------------------+
| ``gesis``  | ``mh``       | ``123``    |           | Username for Methods Hub.                                                                         |                                |
+------------+--------------+------------+-----------+---------------------------------------------------------------------------------------------------+--------------------------------+
| ``gesis``  | ``mhowner``  | ``123``    | ``owner`` | Username for Methods Hub.                                                                         |                                |
+------------+--------------+------------+-----------+---------------------------------------------------------------------------------------------------+--------------------------------+

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
