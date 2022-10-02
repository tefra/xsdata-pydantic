.. include:: ../README.rst
    :start-line: 3

Why Pydantic?
=============

Because you asked for! Pydantic offers out of the box validations and offers a
dataclasses compatibility layer that we utilize to bring code generation and
xml data binding with xsdata!


Limitations
===========


Pydantic dataclasses don't behave with nested classes and self referencing types.

Check `issue <https://github.com/samuelcolvin/pydantic/issues/3695>`_ on github.
Until this issue is fixed, you can use the xsdata generator `--unnest-classes`
flag, that will move nested classes to the root level.


.. code:: console

    xsdata SOURCE --unnest-classes --output pydantic

There is still some issues with forward references but most of the xsdata-samples
tests are passing.


The plugin is using xsdata's data bindings to parse json/xml, only xsdata's
:ref:`types <xsdata:Data Types>` are supported!


.. toctree::
    :maxdepth: 1
    :hidden:

    installation
    codegen
    bindings
    changelog
    GitHub Repository <https://github.com/tefra/xsdata-pydantic>


.. meta::
   :google-site-verification: VSyrlSSIOrwnZhhAo3dS6hf1efs-8FxF3KezQ-bH_js
