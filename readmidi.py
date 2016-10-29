#!/usr/bin/env python2
##

import midi
import os
import sys
import pickle
import numpy as np

def getBpm(pattern):
  for track in pattern:
    for n in track:
      if n.metacommand == 0x51:
        print "bpm:", n.get_bpm(), " mpqn:", n.get_mpqn()
        return n.get_bpm()
  raise Exception("No bpm found");

def getMPQN(pattern):
  for track in pattern:
    for n in track:
      if n.metacommand == 0x51:
        print "bpm:", n.get_bpm(), " mpqn:", n.get_mpqn()
        return n.get_mpqn()
  raise Exception("No bpm found");

#microseconds per quarter-note
#beats per minute
#MICROSECONDS_PER_MINUTE = 60000000
#The Resolution is also known as the Pulses per Quarter note (PPQ).

#BPM = MICROSECONDS_PER_MINUTE / MPQN
#MPQN = MICROSECONDS_PER_MINUTE / BPM

#ms per tick
# MSPT: MPQN / RESOLUTION

#A tick represents the lowest level resolution of a MIDI track. Tempo is always analogous with Beats per Minute (BPM) which is the same thing as Quarter notes per Minute (QPM). The Resolution is also known as the Pulses per Quarter note (PPQ). It analogous to Ticks per Beat (TPM).

def tickToUs(mpqn, resolution, tick):
  mspt = mpqn / resolution
  return tick * mspt

#1000 val / 10sec
#100val / sec
def UsToReso(us):
  return int(us / 1000 / 100)

#0-127 -> 0 -> 1
def pitchToFloat(pitch):
  return pitch / 127.

def decodeFile(filename):
  print filename
  pattern = midi.read_midifile(filename)
  pattern.make_ticks_abs()
  discarded = 0
  mpqn = getMPQN(pattern)
  bpm = getBpm(pattern)
  print "resolution:", pattern.resolution
  #print pattern

  #1000
  result = [0] * 100

  for track in pattern:
    for n in track:
      #print n
      if n.is_event(0x90): #NOTEON_EV
        if n.channel != 9:
          discarded += 1
          continue
        if n.velocity == 0:
          continue #note off
        us = tickToUs(mpqn, pattern.resolution, n.tick)
        r = UsToReso(us)
        if r >= 100:
          continue
        #print "Note:", us, " t:", n.pitch, "r:", r
        result[r] = pitchToFloat(n.pitch)
  #print "Result:", result
  print "## DISCARDED NOTE:", discarded
  return { "data": result, "bpm": bpm / 1000. }



def walkFiles(dir):
  dataset = []
  for dirpath, dnames, fnames in os.walk(dir):
    for f in fnames:
      if f.endswith(".mid"):
        r = decodeFile(os.path.join(dirpath, f))
        dataset.append(r)
  with open('data.pkl', 'wb') as out:
    pickle.dump(dataset, out, 2)

  #print dataset
if __name__ == "__main__":
  f = sys.argv[1]
  walkFiles(f);
