# Passwd Parsing
Utility for parsing the UNIX /etc/passwd and /etc/groups files and combine the data into a single json output
- If any line fails to parse it will be ignored
- Check for stderr and return code to see if there are any validation issues

# Usage
passwd-parser [-h] [-p path] [-g path] [-i number]

optional arguments:
-  -h, --help - show this help message and exit
-  -p path, --passwd path - override default /etc/passwd location
-  -g path, --group path - override default /etc/group location
-  -i number, --indent number - formats json, omit for single line output

# Testing
Before moving passwd-parser into your /bin folder make sure to test it: 
- default test with your local /etc/passwd and /etc/group 
- test with synthetic data to make sure errors are correctly reported

```
$ python tests.py
test_default (__main__.PasswdParserTests) ... ok
test_synthetic (__main__.PasswdParserTests) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.123s

OK
```


## Supported python versions
- 2.7
- 3.5

## Revisions
- 1.0 initial release. August 18, 2018

## MIT Lincense
This project is licensed under the terms of the MIT license

Copyright (c) 2018 Philip Peshin