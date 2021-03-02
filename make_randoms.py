#!/usr/bin/env python
import sys
import numpy as np

if __name__ == "__main__":
    try:
        nr = int(sys.argv[1])
        Lbox = float(sys.argv[2])
        seed = int(sys.argv[3])
        fname = sys.argv[4]
    except IndexError:
        print("Usage: make_randoms.py <number of randoms> <Lbox size in Mpc/h> <integer seed to use> <output file name>")
        exit()

    np.random.seed(seed)
    data = np.random.random((nr, 3)) * Lbox
    np.savetxt(fname, data, fmt="%3.4f")
