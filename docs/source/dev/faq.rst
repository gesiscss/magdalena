.. SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
.. SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
..
.. SPDX-License-Identifier: AGPL-3.0-or-later

Frequently Asked Questions
--------------------------

#. Run the test collection takes too long. Why?

   Some of the tests requires the creation of a Docker image. This step is know to be slow. We avoid to create the Docker image when it is not necessary.
