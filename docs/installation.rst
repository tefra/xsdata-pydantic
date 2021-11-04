Installation
============

Install using pip
-----------------

The recommended method is to use a virtual environment.

.. code-block:: console

    $ pip install xsdata-pydantic[cli,lxml,soap]

.. hint::

     - Install the cli requirements for the code generator
     - Install the soap requirements for the builtin wsdl client
     - Install lxml if you want to use one of the lxml handlers/writers instead of
       the builtin python xml implementations.

In order to use the latest updates you can also install directly from the git repo.

.. code-block:: console

    $ pip install git+https://github.com/tefra/xsdata-pydantic@master#egg=xsdata-pydantic[cli]


Install using conda
-------------------

.. code-block:: console

    $ conda install -c conda-forge xsdata-pydantic
