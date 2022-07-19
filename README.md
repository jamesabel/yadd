# yadd

Yet Another `dict` Differ

# Debug aid

`yadd` helps you debug your dict differences. It pinpoints the values that are different to aid in debugging.

# Close enough

You may have heard the term "close enough for Jazz". Well, that can apply to floating point numbers too. yadda uses `cmath.isclose()`
for numbers.

# Lots of data types

- iterables
  - dict
  - list
  - tuple
- numbers
  - int, float, complex, Decimal
- str
- bool

# Make your own yadda-yadda

`yadd` has several parameters, most of which are dependent on the usage model. You may want to consider writing your own
function that calls yadda with the parameters most appropriate for your usage.

Example:

```python

from yadd import yadd

def my_yadd(*args, **kwargs) -> bool:
    return yadd(*args, rel_tol=1E-6, abs_tol=1E-9, **kwargs)

```

# Related Solutions

[DeepDiff](https://github.com/seperman/deepdiff)
