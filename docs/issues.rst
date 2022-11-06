Common Issues
=============

Pydantic has a compatibility layer to work with dataclasses but there are some
known issues.


Nested Classes
--------------

If you get value errors or forward res errors, try to generate your models
with the flag `--unnest-classes`. This will move all nested classes to the
root level.


.. code:: console

    xsdata SOURCE --unnest-classes --output pydantic


There are still some issues with self referencing types, check
`issue <https://github.com/samuelcolvin/pydantic/issues/3695>`_ on github.


Missing Validators
------------------

This plugin will register all the custom validators for the xsdata
builtin types like XmlDuration or XmlDate but it's important to load
the plugin before using the models, otherwise you will get an error like
this

.. code:: python

    RuntimeError: no validator found for <class 'xsdata.models.datatype.XmlDuration'>, see `arbitrary_types_allowed` in Config


Loading a serializer or parser is enough for the hook to run.

.. code:: python

    from pydantic.dataclasses import dataclass
    from xsdata.models.datatype import XmlDuration
    # import serializer to trigger the xsdata hook to register the validators
    from xsdata_pydantic.bindings import XmlSerializer

    @dataclass
    class DurationRangeMatcherType:
        begin: XmlDuration

    print(DurationRangeMatcherType(begin=XmlDuration("PT3S")))
