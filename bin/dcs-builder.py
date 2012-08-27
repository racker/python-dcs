#!/usr/bin/env python

import sys
import os
from optparse import OptionParser

from dcs import base

def main():
    usage = 'usage: %prog [--validate] --source=<path to the directory ' + \
            'with attributes files> --output=<output directory>'
    parser = OptionParser(usage=usage)
    parser.add_option('--source', dest='source',
                      help='Path to directory containing attributes files')
    parser.add_option('--output', dest='output',
                      help='Output directory')
    parser.add_option('--validate', dest='validate', action='store_true',
                      help='Validate the JSON attribute files')

    (options, args) = parser.parse_args()

    if not options.validate and not (options.source and options.output):
      parser.print_usage()
      sys.exit(1)

    if not os.path.exists(options.source):
        raise Exception('Source directory must exist')

    if options.validate:
        base.runit(options.source, None, dry_run=True)
    else:
        if not os.path.exists(options.output):
            os.makedirs(options.output)

        base.runit(options.source, options.output)

if __name__ == '__main__':
    main()
