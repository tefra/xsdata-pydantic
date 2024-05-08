# Code Generation

All the xsdata [cli](https://xsdata.readthedocs.io/en/latest/codegen/intro/) features
are available. You only need to specify **pydantic** as the output format

## Example from Schema

```console
$ xsdata tests/fixtures/schemas/po.xsd --output pydantic --package tests.fixtures.po.models --structure-style single-package
Parsing schema po.xsd
Compiling schema po.xsd
Builder: 6 main and 1 inner classes
Analyzer input: 6 main and 1 inner classes
Analyzer output: 5 main and 1 inner classes
Generating package: init
Generating package: tests.fixtures.po.models
```

## Example with config

```console
$ xsdata tests/fixtures/schemas/po.xsd --config tests/fixtures/pydantic.conf.xml
Parsing schema po.xsd
Compiling schema po.xsd
Builder: 6 main and 1 inner classes
Analyzer input: 6 main and 1 inner classes
Analyzer output: 5 main and 1 inner classes
Generating package: init
Generating package: tests.fixtures.po.models
```

```xml
--8<-- "tests/fixtures/pydantic.conf.xml"
```

## Generated Models

```python
--8<-- "tests/fixtures/po/models.py"
```
