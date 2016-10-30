#!/usr/bin/env python3
##

import pickle
import sys
import numpy as np

def importFile(f):
  with open('data.pkl', 'rb') as inf:
    dataset = pickle.load(inf, encoding='latin1')
    return dataset

def readData(f):
  d = importFile(f)
  return convert(d)

def convert(d):
  IN = []
  OUT = []
  for data in d:
    IN.append(data["data"])
    OUT.append(data["bpm"])
  return (np.array(IN), np.array([OUT]).transpose())

if __name__ == "__main__":
  a,b = readData(sys.argv[1])
  print(b)
  #print(IN)
  #print(OUT)
  #print(d)
