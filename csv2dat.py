#!/usr/bin/env python3

"""
convert csv to tabular data
"""

import sys
import csv

stdin = csv.reader(sys.stdin)

for ln in stdin:
    ln = (x.strip() for x in ln)
    ln = (str(x) for x in ln)
    ln = (x.replace(',','') for x in ln)
    print('\t'.join(ln))
