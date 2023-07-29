# Instrument Price Checker

A proof of concept command line application that receives
an rfq as input and outputs the associated price.

## Prerequisites

Have Python 3.10 (or later) and pip (preferably latest)
installed: https://www.python.org/downloads/

Create a virtual environment and activate it:
```commandline
python3 -m venv <path_to_venv>
source <path_to_venv>/bin/activate
```

Install the project's dependencies into the virtual environment:
```commandline
pip install -r requirements.txt
```

## Usage

As this application is only a proof of concept, it
accepts 3 valid rfqs as input (other inputs will not be
valid or they will raise a 404 error):
```text
"fx_spot FX_INSTRUMENT 25 john.doe@gmail.com"
"gold_call GOLD_INSTRUMENT 1 john.doe@gmail.com"
"bond BOND_INSTRUMENT 20 john.doe@gmail.com"
```

To run the application, run the following command:
```commandline
python3 app.py --rfq=<valid_rfq>
```

## Testing and Coverage

To run the tests, you should run this command:
```commandline
coverage run -m pytest tests
```

Then, run the command below to see the coverage report:
```commandline
coverage report -m
```

You should get this report:
```text
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
app.py                         23      1    96%   45
enums/rfq.py                   11      0   100%
logger/__init__.py              1      0   100%
logger/logger.py               14      0   100%
schemas/rfq_schema.py          10      0   100%
tests/__init__.py               0      0   100%
tests/test_integration.py      40      0   100%
tests/test_unit.py             53      0   100%
utils/price.py                  8      0   100%
validators/rfq.py              15      0   100%
---------------------------------------------------------
TOTAL                         175      1    99%
```
