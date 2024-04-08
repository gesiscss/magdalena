.. SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
.. SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
..
.. SPDX-License-Identifier: AGPL-3.0-or-later

Architecture
============

Diagram
-------

.. figure:: img/magdalena.drawio.png
   :alt: Diagram of magdalena

   Diagram of magdalena

The host machine shares ``/var/run/docker.sock`` with the ``magdalena``
container (sometimes called Docker outside of Docker or Dood that should
not be mistake by Docker in Docker or DinD). The container running
`Quarto <https://quarto.org/>`__ is a sibling container.
