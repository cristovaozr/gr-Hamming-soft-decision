#!/usr/bin/env python3

import math
import sys

def main():
    fname1 = sys.argv[1]
    fname2 = sys.argv[2]

    with open(fname1, 'rb') as f1:
        d1 = f1.read(1024*1024)

    with open(fname2, 'rb') as f2:
        d2 = f2.read(1024*1024)

    diffs = [a^b for a,b in zip(d1, d2)]
    print("A relação entre o total de bits diferentes e o total é: {}".format(sum(diffs)/len(diffs)))

    return 0


if __name__ == "__main__":
    sys.exit(main())
