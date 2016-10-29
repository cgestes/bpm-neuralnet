#!/usr/bin/env python3
##

import pickle
import sys
import numpy as np

def importFile(f):
  with open('data.pkl', 'rb') as inf:
    dataset = pickle.load(inf)
    return dataset

if __name__ == "__main__":
  d = importFile(sys.argv[1])
  IN = []
  OUT = []
  for data in d:
    IN.append(data["data"])
    OUT.append(data["bpm"])
  print np.array(IN)
  print np.array(OUT)
  #print(d)
