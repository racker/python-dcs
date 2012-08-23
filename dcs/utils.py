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

from __future__ import with_statement

try:
    import simplejson as json
except:
    import json

from copy import deepcopy

__all__ = ['merge_dictionary', 'file_to_context']


def merge_dictionary(dst, src, merge_list_keys=None):
    """
    Merge a dictionary, and if there are any lists with matching keys, append
    them.
    """
    if merge_list_keys == None:
        merge_list_keys = []

    src = deepcopy(src)
    stack = [(dst, src)]
    while stack:
        current_dst, current_src = stack.pop()
        for key in current_src:
            if key not in current_dst:
                current_dst[key] = current_src[key]
            else:
                if isinstance(current_src[key], dict) and \
                   isinstance(current_dst[key], dict):
                    stack.append((current_dst[key], current_src[key]))
                elif key in merge_list_keys:
                    if isinstance(current_src[key], list) and \
                       isinstance(current_dst[key], list):
                        current_dst[key].extend(current_src[key])
                    else:
                        raise TypeError('key %s was not of list types '
                              '(source: %s dest: %s)' % (key,
                              type(current_src[key]), type(current_dst[key])))
                else:
                    current_dst[key] = current_src[key]
    return dst


def file_to_context(filename):
    file_contents = None
    with open(filename, 'r') as fp:
        file_contents = fp.read()
    file_data = None
    try:
        file_data = json.loads(file_contents)
    except SyntaxError, e:
        e.filename = filename
        raise
    except Exception, e:
        e.filename = filename
        raise
    return file_data
