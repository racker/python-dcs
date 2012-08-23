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
