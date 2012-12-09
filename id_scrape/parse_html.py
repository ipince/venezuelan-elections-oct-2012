#!/usr/bin/python

import os
import time

count = 0 
cache_dir = 'cache/00/000'
for filename in sorted(os.listdir(cache_dir)):
  print filename
  print "mtime %s" % time.ctime(os.path.getmtime(os.path.join(cache_dir, filename)))
  count += 1
  if (count > 10): break
