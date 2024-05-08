# Common Issues

## Nested Classes

If you get value errors or forward reference errors, try to generate your models with
the flag `--unnest-classes`. This will move all nested classes to the root level.

```console
xsdata SOURCE --unnest-classes --output pydantic
```

## Missing Validators

This plugin will register all the custom validators for the xsdata builtin types like
XmlDuration or XmlDate, but it's important to load the plugin before using the models,
otherwise you will get an error like this

Loading a serializer or parser is enough for the hook to run.

```python
from pydantic.dataclasses import dataclass
from xsdata.models.datatype import XmlDuration
# import serializer to trigger the xsdata hook to register the validators
from xsdata_pydantic.bindings import XmlSerializer

@dataclass
class DurationRangeMatcherType:
    begin: XmlDuration

print(DurationRangeMatcherType(begin=XmlDuration("PT3S")))
```
