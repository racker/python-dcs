# Copyright 2012 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import testutils

from dcs.utils import merge_dictionary, file_to_context

class TestMergeDict(unittest.TestCase):

    def test_merge_dictionary_basic(self):
        dest = {'foo': 1, 'blah': 99}
        src = {'bar': 2, 'blah': 20}
        merge_dictionary(dest, src)
        self.assertEqual(1, dest['foo'])
        self.assertEqual(2, dest['bar'])
        self.assertEqual(20, dest['blah'])
        self.assertEqual(sorted(['foo', 'bar', 'blah']), sorted(dest.keys()))

    def test_merge_dictionary_deep(self):
        dest = {'foo': 1, 'bar': {'cats': 'dogs'}, 'deep': {'deeper': [1,2]}}
        src = {'blah': 2, 'bar': {'meow': 'woof'}, 'deep': {'deeper': [3,4]}}
        merge_dictionary(dest, src, merge_list_keys=['deeper'])
        self.assertEqual(1, dest['foo'])
        self.assertEqual(2, dest['blah'])
        self.assertEqual(sorted(['foo', 'bar', 'blah', 'deep']), sorted(dest.keys()))
        self.assertEqual({'cats': 'dogs', 'meow': 'woof'}, dest['bar'])
        self.assertEqual({'deeper': [1,2,3,4]}, dest['deep'])

    def test_merge_dictionary_invalid_append(self):
        dest = {'foo': [1]}
        src = {'foo': 2}
        with self.assertRaises(TypeError) as e:
            merge_dictionary(dest, src, merge_list_keys=['foo'])

    def test_merge_dictionary_append(self):
        dest = {'foo': [1]}
        src = {'foo': [2]}
        merge_dictionary(dest, src, merge_list_keys=['foo'])
        self.assertEqual(sorted([1,2]), sorted(dest['foo']))

class TestFileToContext(unittest.TestCase):

    def setUp(self):
        self.fixtures = testutils.fixturesLoader('filecontext')

    def test_simple(self):
        data = file_to_context(self.fixtures.path('basic.py'))
        self.assertEqual(1, data['foo'])
        self.assertEqual('some string', data['blah'])
        self.assertEqual([1,2,3], data['bar'])

    def test_syntax_error(self):
        with self.assertRaises(Exception) as e:
            file_to_context(self.fixtures.path('syntax_error.py'))

if __name__ == '__main__':
    unittest.main()


