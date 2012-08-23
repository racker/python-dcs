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

import os
import sys
from distutils.core import setup
from os.path import join as pjoin


def read_version_string():
    version = None
    sys.path.insert(0, pjoin(os.getcwd()))
    from dcs import __version__
    version = __version__
    sys.path.pop(0)
    return version

pre_python26 = (sys.version_info[0] == 2 and sys.version_info[1] < 6)

setup(
    name='dcs',
    version=read_version_string(),
    description='Dynamic Chef Solo provides an easier to produce the JSON ' +
                'attributes used by Chef Solo.',
    author='Rackspace, Inc.',
    author_email='paul.querna@rackspace.com',
    requires=([], ['simplejson'],)[pre_python26],
    scripts=['bin/dcs-builder.py'],
    packages={
        'dcs': 'dcs'
    },
    package_dir={
        'dcs': 'dcs',
    },
    license='Apache License (2.0)',
    url='https://github.com/racker/python-dcs',
    cmdclass={},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy'])
