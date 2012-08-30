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


import re
import os
import sys
from collections import defaultdict
from os.path import join as pjoin
from os.path import basename
from glob import glob
from copy import deepcopy

try:
    import simplejson as json
except:
    import json


from dcs.utils import merge_dictionary, file_to_context


class Resource(object):
    def __init__(self):
        self.output = {}

    def merge(self, resource):
        merge_dictionary(self.output, resource.output,
                         merge_list_keys=['run_list'])

    def load(self, path):
        data = file_to_context(path)
        merge_dictionary(self.output, data, merge_list_keys=['run_list'])


class Node(Resource):
    def __init__(self, hostname, info=None):
        super(Node, self).__init__()
        self._hostname = hostname
        self.output['fqdn'] = self._hostname
        self.output['domain'] = self._hostname[self._hostname.find('.') + 1:]
        self.output['name'] = self._explode_hostname()['hostname']
        self.output['info'] = info or {}

    def _explode_hostname(self):
        # ord1-maas-prod-api0.cm.k1k.me
        match = re.match(r"^(?P<datacenter>\w+)(?P<datacenter_number>\d+)-(?P<product>\w+)-(?P<environment>\w+)-(?P<purpose>\w+)(?P<purpose_number>\d+)(\..*){0,1}$", self._hostname)
        if match is None:
            raise Exception('Unable to parse hostname: ' + self._hostname)

        return {
            'product': match.group('product'),
            'environment': match.group('environment'),
            'region': match.group('datacenter'),
            'datacenter': '%s%s' % (match.group('datacenter'),
                                    match.group('datacenter_number')),
            'purpose': match.group('purpose'),
            'hostname': '%s%s-%s-%s-%s%s' % match.groups()[0:6]
        }

    def save(self, path):
        data = json.dumps(self.output, sort_keys=True, indent=4)
        with open(path, 'w') as fp:
            fp.write(data)


class ResourceGather(object):
    sections_map = {
        'product': 'products',
        'environment': 'environments',
        'region': 'regions',
        'datacenter': 'datacenters',
        'purpose': 'purposes'
        }

    def __init__(self):
        self._resources = defaultdict(dict)
        self._nodes = []

    def load(self, rootpath):
        for section, directory in self.sections_map.items():
            spath = pjoin(rootpath, directory, '*.dyp')
            for dyp in glob(spath):
                r = Resource()
                r.load(dyp)
                bname = basename(dyp)[:-4]
                self._resources[section][bname] = r

        spath = pjoin(rootpath, 'nodes', '*.dyp')
        for dyp in glob(spath):
            hostname = basename(dyp)[:-4]
            node_info_path = pjoin(rootpath, 'nodes-info/', hostname + '.dyp')

            if os.path.exists(node_info_path):
                with open(node_info_path, 'r') as fp:
                    info = json.load(fp)
            else:
                info = None

            n = Node(hostname, info)
            n.load(dyp)
            self._nodes.append(n)

    def get_merged_nodes(self):
        for node in self._nodes:
            ni = node._explode_hostname()
            for section, _ in self.sections_map.items():
                if section not in self._resources:
                    continue

                resource = self._resources[section].get(ni[section], None)
                if resource:
                    node.merge(resource)

        for current_node in self._nodes:
            current_node.output['peers'] = []
            for node in self._nodes:
                if node._hostname != current_node._hostname:
                    nout = deepcopy(node.output)
                    nout.pop('peers', None)
                    current_node.output['peers'].append(nout)
        return self._nodes


def runit(inputdir, outputdir, dry_run=False):
    rg = ResourceGather()

    try:
        rg.load(inputdir)
    except Exception, e:
        print e
        print 'Syntax error in file: %s' % (e.filename)
        print str(e)
        sys.exit(1)

    nodes = rg.get_merged_nodes()

    if dry_run:
        print 'No syntax error detected'
        return

    for n in nodes:
        outpath = pjoin(outputdir, n._hostname) + '.json'
        print 'Saving %s' % outpath
        n.save(outpath)
