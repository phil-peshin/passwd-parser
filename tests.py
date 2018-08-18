#!/usr/bin/env python
from __future__ import print_function
import unittest, json, tempfile
from subprocess import Popen, PIPE, STDOUT, check_output

# loads json  and reformats in consistent way through sorting to canonical form
def load_json(content):
    return json.dumps(json.loads(content), sort_keys=True)

# loads text and reformats in consistent way through sorting
def load_text(content):
    return '\n'.join(sorted(content.strip().split('\n')))

# executes command and reformats stdout/stderr to canonical form
def execute(command):
    p = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    output, stderr = p.communicate()
    return p.returncode, load_json(output.decode('utf-8')), load_text(stderr.decode('utf-8'))

class PasswdParserTests(unittest.TestCase):

    # executes passwd-parser without arguments and checks for expected results
    def test_default(self):
        returncode, stdout, stderr = execute('./passwd-parser')
        self.assertEqual(returncode, 0)
        self.assertFalse(stderr)

    # executes passwd-parser with various test data and checks for expected results
    def test_synthetic(self):
        for data in testdata:
            with tempfile.NamedTemporaryFile(mode='w') as passwd, tempfile.NamedTemporaryFile(mode='w') as group:
                passwd.write(data['passwd'].strip())
                passwd.flush()
                group.write(data['group'].strip())
                group.flush()
                returncode, stdout, stderr = execute('./passwd-parser -p %s -g %s' % (passwd.name, group.name))
                self.assertEqual(returncode, data['returncode'])
                self.assertEqual(stdout, load_json(data['stdout']))
                self.assertEqual(stderr, load_text(data['stderr']))

#
# Data for unit tests:
# - passwd file content
# - group file content
# - expected stdout
# - expected stderr
# - expected returncode
#
testdata = [
    # good data
dict(
    passwd='''
nobody:x:1000:1000:Nobody:
user1001:x:1001:1001:User 1:/bin/bash
user1002:x:1002:1002:User 2:/bin/bash
''',
    group='''
group1:x:1:user1001
group2:x:2:user1002
group3:x:3:user1001,user1002
''',
    stdout='''
{
  "nobody": {
    "groups": [],
    "full_name": "Nobody",
    "uid": "1000"
  },
  "user1002": {
    "groups": [
      "group2",
      "group3"
    ],
    "full_name": "User 2",
    "uid": "1002"
  },
  "user1001": {
    "groups": [
      "group1",
      "group3"
    ],
    "full_name": "User 1",
    "uid": "1001"
  }
}
''',
    stderr='',
    returncode=0
),
    # invalid data
dict(
    passwd='''
nobody:x:1000:1000:Nobody:
user100:x:1001:1001:User 1:/bin/bash
user1002:x:1002:1002:User 2:/bin/bash
dummy:x
''',
    group='''
group1:x:1:user1001
group2:x:2:user1002
group3:x:3:user1001,user1002
group4:x:
''',
    stdout='''
{
  "nobody": {
    "groups": [],
    "full_name": "Nobody",
    "uid": "1000"
  },
  "user1002": {
    "groups": [
      "group2",
      "group3"
    ],
    "full_name": "User 2",
    "uid": "1002"
  },
  "user100": {
    "groups": [],
    "full_name": "User 1",
    "uid": "1001"
  }
}
''',
    stderr='''
passwd line #4 invalid
group line #4 invalid
group line #1 user not found: user1001
group line #3 user not found: user1001
''',
    returncode=1
)
]


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PasswdParserTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
