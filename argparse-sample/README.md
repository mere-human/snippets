# Argparse sample

This is a sample of command line options parsing using _argparse_ Python package.

**Motivation:** It is easier just to copy from sample. Documentation is obscure and I don't remember all the tricks. 

**Usage:**
```sample.py -h
usage: sample.py [-h] [-f] --val VAL [--var {1,3,5}] [--push X] [-i | -e]
                 [--version]
                 N1 [N2 [N2 ...]]

Argparse sample

positional arguments:
  N1             positional, metavar, required
  N2             positional, zero or more

optional arguments:
  -h, --help     show this help message and exit
  -f, --flag     short name, store true
  --val VAL      required, store arg value
  --var {1,3,5}  choices (default: 3)
  --push X       append value, custom attribute name
  -i             can not be used with -e
  -e             can not be used with -i
  --version      prints version and exits
```

**TODO:**
* unit tests
* automatically update usage from script output