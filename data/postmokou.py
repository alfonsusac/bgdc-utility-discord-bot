import os
from itertools import chain
from glob import glob

filename = './data/mokoutext.json'
filenameout = './data/mokoutextpost.json'

with open(filename, 'r') as fileinput:
     for line in fileinput:
          line = line.lower()
          with open(filenameout, 'a') as out:
               out.writelines(line)
