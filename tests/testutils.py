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

import sys
import os
from os.path import join as pjoin


THIS_DIR = os.path.abspath(os.path.split(__file__)[0])
ROOT_DIR = os.path.dirname(THIS_DIR)

sys.path.insert(0, pjoin(ROOT_DIR, 'pylib'))

class Fixtures(object):
    def __init__(self, path):
        self.root_path = os.path.abspath(path)

    def path(self, appendPath):
        return pjoin(self.root_path, appendPath)

    def contents(self, appendPath):
        filename = self.path(appendPath)
        with open(filename, 'r') as fp:
            return fp.read()

def fixturesLoader(path):
    p = Fixtures(pjoin(THIS_DIR, 'fixtures', path))
    return p

if __name__ == "__main__":
    import coverage
    from unittest import TestLoader, TestSuite, TextTestRunner


    cov = coverage.coverage(config_file=pjoin(THIS_DIR, '.coveragerc'))
    cov.start()

    loader = TestLoader()
    tests = loader.discover(THIS_DIR)
    suite = TestSuite(tests)
    runner = TextTestRunner()

    runner.run(suite)

    cov.stop()
    cov.save()
    cov.html_report()
