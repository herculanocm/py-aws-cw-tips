# Py tips for use
de_aws_cw_tips = Data Engineer AWS CloudWatch Python Tips
## Using:

First generate wheel file for install with
```
python setup.py bdist_wheel
```

Import the module
```
from de_aws_cw_tips import cw_utils as CW
```

## Enviroments

* Python >= 3.7

## Tests

```
pytest -v -s
```