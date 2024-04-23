Unit Tests
==========

Unit tests are located in ``magdalena/tests/unit/``. To run the unit tests, execute

.. code-block:: bash

    pytest \
    --capture=no \
    --verbose \
    --log-cli-level=INFO \
    magdalena/tests/unit/

.. important::

    Because tests can take a long time to complete, we recommend to enable the `live logs <https://docs.pytest.org/en/7.1.x/how-to/logging.html#live-logs>`_ with ``--log-cli-level=INFO``.
