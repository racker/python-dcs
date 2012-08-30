import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import testutils

from dcs.base import Node

class TestExplodeHostname(unittest.TestCase):

    def test_explode_hostname_short(self):
        n = Node("ord1-maas-prod-api0")
        data = n._explode_hostname()
        self.assertEqual('ord', data['region'])
        self.assertEqual('api', data['purpose'])
        self.assertEqual('ord1-maas-prod-api0', data['hostname'])
        self.assertEqual('ord', data['region'])

    def test_explode_hostname_full(self):
        n = Node("ord1-maas-prod-api0.cm.k1k.me")
        data = n._explode_hostname()
        self.assertEqual('ord', data['region'])
        self.assertEqual('api', data['purpose'])
        self.assertEqual('ord1-maas-prod-api0', data['hostname'])
        self.assertEqual('ord', data['region'])

    def test_explode_hostname_invalid(self):
        with self.assertRaises(Exception) as e:
            n = Node("ord1-maas-")

if __name__ == '__main__':
    unittest.main()


