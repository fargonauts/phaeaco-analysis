#!/usr/bin/env python3

import csv
import pandas as ps

from pprint import pprint
from collections import OrderedDict

bad_val = None

def convert(v):
    v = v.strip()
    if v == 'None' or v == '':
        v = bad_val
    elif '.' in v:
        v = float(v)
    else:
        v = int(v)
    return v

def read(includeNone=False):
    with open('data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        data = [row for row in reader]

    # Works... but cleaner data is desired.
    # pprint(pandas.DataFrame([row[1:] for row in data[1:]]))

    data = [row[1:] for row in data[1:]]
    headers = data[0]
    common_headers = headers[1:9]
    data = data[1:]
    bps      = []
    subjects = []
    statistics = {k : list() for k in common_headers}

    continued = False
    for row in data:
        bp = int(row[0])
        skipped = False
        for i, (k, v) in enumerate(zip(headers[1:], row[1:])):
            v = convert(v)
            if i == 0:
                if not includeNone and v == bad_val:
                    skipped = True
                    continue
                bps.append(bp)
                subjects.append('human')
            if i == 8:
                if not includeNone:
                    if v == bad_val:
                        skipped = True
                        continue
                    else:
                        skipped = False
                bps.append(bp)
                subjects.append('phaeaco')

            if not skipped:
                statistics[k].append(v)

    print(len(bps))
    print(len(subjects))
    print([(k, len(subl)) for k, subl in statistics.items()])

    return ps.DataFrame(dict(**{'bongard problems' : bps,
                                'subjects'         : subjects}, **statistics))
