#!/usr/bin/env python3
##

import pickle
import sys

def importFile(f):
  with open('data.pkl', 'rb') as inf:
    dataset = pickle.load(inf)
    return dataset

if __name__ == "__main__":
  d = importFile(sys.argv[1])
  print(d)
