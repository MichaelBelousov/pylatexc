#!/usr/bin/env python3

"""
convert csv to tabular data
"""

import sys
import csv

stdin = csv.reader(sys.stdin)

for ln in stdin:
    print('\t'.join((x.strip() for x in ln)))
