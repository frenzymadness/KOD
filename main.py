#!/usr/bin/env python

# import modulu
import re

# Regularni vyraz  pro parsing radku z logu
parser = re.compile('(\d+\.\d+\.\d+\.\d+) - - (\[.+ .+\]) (".+") (\d+ \d+) (".+") (".+")')

# Pripona pro komprimovane soubory
cmp_suffix = '.cmp'
dcmp_suffix = '.dcmp'


def compress(logfile):

    # pomocna pole
    original = []
    output = []
    hash_table = {}

    # nacteni vstupnich dat do pole
    with open(logfile, 'r') as f:
        for line in f:
            original.append(parser.match(line).groups())

    # Samotna komprese
    # Pro kazdy radek pridame zaznam do vysledku
    for row_num, row_content in enumerate(original):
        output.append([])
        # Pro kazdou cast jednoho zaznamu
        for part_num, part_content in enumerate(row_content):
            # Pokud je cast vetsi nez ctyri znaky, provedeme kompresi
            if len(part_content) > 4:
                # pokud cast v hash tabulce, pouzijeme hash, jinak ji
                # do hash tabulky vlozime a vytvorime pro ni hash
                if part_content in hash_table.keys():
                    output[-1].append(hash_table[part_content])
                else:
                    hash_table[part_content] = "%d#%d" % (row_num, part_num)
                    output[-1].append(part_content)
            # casti mensi nez urcity pocet znaku ignorujeme a jen vkladame do vysledku
            else:
                output[-1].append(part_content)

    #ulozeni vystupu
    with open(logfile+cmp_suffix, 'w') as f:
        for record in original:
            f.write(" ".join(record))

if __name__ == '__main__':
    compress('10.log')
    compress('100.log')
    compress('1000.log')
    compress('10000.log')
    compress('100000.log')
    compress('200000.log')
