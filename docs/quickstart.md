Quickstart
==========

Bulwark is designed to be easy to use and easy to add checks to code
while you're writing it.

First, install Bulwark:

```bash
pip install bulwark
```

Next, import bulwark. You can either use function versions of the checks
or decorator versions. By convension, import either/both of these as
follow:

```
import bulwark.checks as ck
import bulwark.decorators as dc
```

If you've chosen to use decorators to interact with the checks (the
recommended method for checks to be run on each function call), you can
write a function for your project like normal, but with your chosen
decorators on top:

```python
import bulwark.decorators as dc
import pandas as pd


@dc.HasNoNans()
def add_five(df):
    return df + 5


df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
add_five(df)
```

You can stack multiple decorators on top of each other to have the first
failed decorator check result in an assertion error or use the built-in
MultiCheck to collect all of the errors are raise them at once.

See [examples](examples.html) to see more advanced usage.
