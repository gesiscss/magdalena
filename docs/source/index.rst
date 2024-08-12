.. SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
.. SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
..
.. SPDX-License-Identifier: AGPL-3.0-or-later

.. magadalena documentation master file, created by
   sphinx-quickstart on Fri Mar 15 12:18:33 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ``magadalena``'s documentation!
==========================================

``magdalena`` is a microservice to convert
`Quarto <https://quarto.org/>`_ documents into output formats such as
HTML and PDF **for GESIS’ Methods Hub**. ``magdalena`` is the successor of ``andrew``, see https://github.com/GESIS-Methods-Hub/andrew.

The follow sequence diagram illustrates how ``magdalena`` works.

.. mermaid::

   sequenceDiagram
      actor user as User
      participant flask as Web App (Flask)
      participant broker as Broker (RabbitMQ)
      participant worker as Worker (Redis)
      participant backend as Backend (Redis)

      user->>flask: POST /
      flask->>flask: Validate JWT
      flask->>flask: Validate JSON
      flask->>broker: Enqueue new task
      flask->>user: Response with task ID 123
      worker->>broker: Pick task
      worker->>backend: Store result
      user->>flask: GET /result/123
      flask->>broker: Check status of task ID 123
      alt is complete
         flask->>backend: Fetch result
         flask->>user: Response with result
      else
         flask->>user: Response with status
      end


.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   user/api
   user/faq

.. toctree::
   :maxdepth: 2
   :caption: Container Image Documentation

   docker/env

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation

   dev/architecture
   dev/contributing
   dev/unit-tests
   dev/integration-tests
   dev/faq

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
