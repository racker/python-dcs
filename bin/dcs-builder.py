#!/usr/bin/env python

import sys
import os

from dcs import base

def main():
    if len(sys.argv) != 3:
        raise Exception('Invalid Arguments: dcs-builder.py <source_path> <output_path>')

    srcdir = sys.argv[1]
    outdir = sys.argv[2]

    if not os.path.exists(srcdir):
        raise Exception('Source directory must exist')

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    base.runit(srcdir, outdir)

if __name__ == '__main__':
    main()
