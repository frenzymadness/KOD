#!/usr/bin/env python

# import modulu
import re
import time
import os

# Regularni vyraz  pro parsing radku z logu (je mozno zvolit ztratovy, kde se nebere vse v potaz)
#parser = re.compile('(\d+\.\d+\.\d+\.\d+) - - (\[.+ .+\]) (".+") (\d+ \d+) (".+") (".+") (.*)')
# nebo bezztratovy, kde se bere v potaz vse
parser = re.compile('(\d+\.\d+\.\d+\.\d+) (- -) (\[.+ .+\]) (".+") (\d+ \d+) (".+") (".+") (.*)')

# Pripona pro komprimovane soubory
cmp_suffix = '.cmp'
dcmp_suffix = '.dcmp'


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s of %s took %0.3f ms' % (f.func_name, args[0], (time2-time1)*1000.0)
        return ret
    return wrap


@timing
def compress(logfile):

    # velikost pred kompresi
    orig_size = os.path.getsize(logfile)

    # pomocna pole
    original = []
    output = []
    hash_table = {}

    # nacteni vstupnich dat do pole
    with open(logfile, 'r') as f:
        for line in f:
            try:
                original.append(parser.match(line).groups())
            except:
                print "Error: No matching line founded while preparing data for compression"
                print line
                original.append([line])

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
                if part_content in hash_table:
                    output[-1].append(hash_table[part_content])
                else:
                    hash_table[part_content] = "%d#%d" % (row_num, part_num)
                    output[-1].append(part_content)
            # casti mensi nez urcity pocet znaku ignorujeme a jen vkladame do vysledku
            else:
                output[-1].append(part_content)

    #ulozeni vystupu
    with open(logfile+cmp_suffix, 'w') as f:
        for record in output:
            f.write("|".join(record) + '\n')

    # komprimovana velikost
    cmp_size = os.path.getsize(logfile+cmp_suffix)
    prc_size = 100 - cmp_size / float(orig_size / 100)

    print 'Original size: %d compressed size: %d compress: %.2f' % (orig_size, cmp_size, prc_size)


@timing
def decompress(compressed_file):

    # jmeno originalu
    name = compressed_file.rstrip(cmp_suffix)

    # velikost pred dekompresi
    orig_size = os.path.getsize(name)

    # vyhledavani hashu
    parser = re.compile('\d+#\d+')

    # pomocna pole
    compressed = []
    output = []

    # nacteni vstupnich dat do pole
    with open(compressed_file, 'r') as f:
        for line in f:
            compressed.append(line.split('|'))

    # Samotna dekomprese
    # Pro kazdy radek pridame zaznam do vysledku
    for row_content in compressed:
        output.append([])
        # Pro kazdou cast jednoho zaznamu
        for part_content in row_content:
            # Pokud je cast komprimovana, zamenime ji za dekomprimovany zaznam
            if parser.match(part_content) is not None:
                row, part = part_content.split('#')
                output[-1].append(compressed[int(row)][int(part)])
            # pokud neni komprimovana, jen ji vlozime do vystupu
            else:
                output[-1].append(part_content)

    #ulozeni vystupu
    with open(name+dcmp_suffix, 'w') as f:
        for record in output:
            f.write(" ".join(record))

    # komprimovana velikost
    dcmp_size = os.path.getsize(name+dcmp_suffix)

    print 'Original size: %d decompressed size: %d difference: %.2f' % (orig_size, dcmp_size, dcmp_size - orig_size)

if __name__ == '__main__':
    compress('10.log')
    compress('100.log')
    compress('1000.log')
    compress('10000.log')
    compress('100000.log')
    compress('200000.log')
    decompress('10.log.cmp')
    decompress('100.log.cmp')
    decompress('1000.log.cmp')
    decompress('10000.log.cmp')
    decompress('100000.log.cmp')
    decompress('200000.log.cmp')
