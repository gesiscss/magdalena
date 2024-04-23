.. SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
.. SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
..
.. SPDX-License-Identifier: AGPL-3.0-or-later

Architecture
============

To install the dependencies that each document requires in a safe and reproducible way, we use `repo2docker <https://github.com/jupyterhub/repo2docker>`_ and `binderhub <https://github.com/jupyterhub/binderhub>`_ (in the format of `mybinder.org <https://mybinder.org>`_).

.. important::

   The container image produced by ``repo2docker`` **must** include `Quarto <https://quarto.org/>`_. This should be done with the use of a ``postBuild`` file, see more details on `"Using Binder With Quarto" <https://quarto.org/docs/projects/binder.html>`_.

Instructions to convert the documents is **not** included in the container image. The instructions are part of ``magdalena`` and shared with the container created by ``repo2docker`` as a `volume <https://docs.docker.com/storage/volumes/>`_.

Container Network
-----------------

The host machine shares ``/var/run/docker.sock`` with the ``magdalena``
container (sometimes called Docker outside of Docker or Dood that should
not be mistake by Docker in Docker or DinD). The container created by ``repo2docker`` running
`Quarto <https://quarto.org/>`__ is a sibling to the ``magdalena`` container.

.. figure:: img/magdalena.drawio.png
   :alt: Diagram of containers on the network.

   Containers are siblings.

The shared folder **must** be readable and writable by any user. This is required because of different users in the containers.

.. _git-repository-as-input:

Git Repository as Input
-----------------------

The workflow here is designed to ensure that ``magdalena`` and ``mybinder.org`` use the same Docker image.

.. mermaid::
   :align: center
   :alt: Diagram of convert document from Git repository.
   :caption: Diagram of convert document from Git repository.
   
   sequenceDiagram
        accTitle: Diagram of convert document from Git repository

        autonumber

        actor User

        User->>magdalena: Request HTML version of document
        magdalena->>Git server: Request Git repository
        Git server->>magdalena: Send Git commits
        magdalena->>magdalena: Extract information from Git repository
        magdalena->>mybinder.org: Request build of Git repository
        mybinder.org->>mybinder.org: Build Docker image
        mybinder.org->>hub.docker.com: Push Docker image
        mybinder.org->>hub.docker.com: Request Docker image
        hub.docker.com->>mybinder.org: Send Docker image
        mybinder.org->>mybinder.org: Start Docker container
        mybinder.org->>magdalena: Send token for Docker container
        magdalena->>mybinder.org: Shutdown Docker container
        magdalena->>hub.docker.com: Request Docker image
        hub.docker.com->>magdalena: Send Docker image
        magdalena->>magdalena: Build HTML
        magdalena->>User: Send HTML

.. important::

   Because the Docker image is pushed to a container registry and pulled twice, this workflow is extremely slow and might take a couple of minutes.

Web Source as Input
-------------------

The workflow here is designed to reuse the code used for :ref:`git-repository-as-input`. 

.. mermaid::
   :align: center
   :alt: Diagram of convert document from web source.
   :caption: Diagram of convert document from web source.
   
   sequenceDiagram
        accTitle: Diagram of convert document from web source

        autonumber

        actor User

        User->>magdalena: Request HTML version of document
        magdalena->>Web source: Request document
        Web source->>magdalena: Send document
        magdalena->>magdalena: Extract information from document
        magdalena->>magdalena: Build Docker image
        magdalena->>magdalena: Build HTML
        magdalena->>User: Send HTML
