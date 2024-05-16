Unit Tests
==========

.. important::

    Remember to execute ``poetry shell`` to active the virtual environment created by Poetry.

Unit tests are located in ``magdalena/tests/unit/``. To run the unit tests, execute

.. code-block:: bash

    pytest \
    --capture=no \
    --verbose \
    --log-cli-level=INFO \
    magdalena/tests/unit/

.. note::

    Because tests can take a long time to complete, we recommend to enable the `live logs <https://docs.pytest.org/en/7.1.x/how-to/logging.html#live-logs>`_ with ``--log-cli-level=INFO``.
