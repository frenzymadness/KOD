#!/usr/bin/env python

# import modulu
import re

# Regularni vyraz  pro parsing radku z logu
parser = re.compile('(\d+\.\d+\.\d+\.\d+) - - (\[.+ .+\]) (".+") (\d+ \d+) (".+") (".+")')

# nazev souboru pro kompresi
logfile = 'small.log'

# pomocna pole
original = []
output = []
hash_table = {}

# nacteni vstupnich dat do pole
with open(logfile, 'r') as f:
    for line in f:
        original.append(parser.match(line).groups())

#print original

for row_num, row_content in enumerate(original):
    output.append([])
    for part_num, part_content in enumerate(row_content):
        if len(part_content) > 4:
            if part_content in hash_table.keys():
                output[-1].append(hash_table[part_content])
            else:
                hash_table[part_content] = "%d#%d" % (row_num, part_num)
                output[-1].append(part_content)
        else:
            output[-1].append(part_content)

#print output
for record in original:
    print " ".join(record)

print "#####################################################"

for record in output:
    print " ".join(record)
