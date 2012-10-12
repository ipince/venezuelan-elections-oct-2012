#!/usr/bin/python

import codecs
import os
import urllib2
import itertools
import random
import time
from collections import defaultdict
from lxml import etree

import db

db = db.DB('venedb_test')
#db.create_tables()

#db.save_person(123, full_name='test name', second_name='ipi')

def cached_url(url, cedula):
  # structure is cache/<2-digit-millions>/<3-digit-thousands>
  filled = str(cedula).zfill(8)
  millions_path = os.path.join('cache', filled[:2])
  thousands_path = os.path.join(millions_path, filled[2:5])
  if not os.path.exists(millions_path):
    os.makedirs(millions_path)
  if not os.path.exists(thousands_path):
    os.makedirs(thousands_path)
  return os.path.join(thousands_path, url[url.find('.ve/')+4:].replace("/", "_").replace(":", "_"))

def fetch_url(cedula):
  base_url = 'http://www.cne.gov.ve/web/registro_electoral/ce.php'
  #base_url = 'http://cne.gob.ve/web/registro_electoral/ce.php'
  url = base_url + '?nacionalidad=V&cedula=' + str(cedula)
  cached = cached_url(url, cedula)
  contents = ""
  if os.path.exists(cached):
    print "Reading from cached file %s" % cached
    contents = file(cached).read()
  else:
    print "Fetching: " + url
    start = time.time()
    contents = urllib2.urlopen(url).read()
    elapsed = time.time() - start
    print "Took %.2f" % elapsed
    outfile = file(cached, 'w')
    outfile.write(contents)
    time.sleep(0.25)
  return etree.HTML(contents)

# Last ID as of 10/11/12 is 27,415,999

millions = range(1, 25)
thousands = range(0, 1000)
tmp = range(0, 1000)
#random.shuffle(tmp)

for thou in range(31, 40):
  for c in tmp:
    cedula = int(str(15) + str(thou).zfill(3) + str(c).zfill(3))
    fetch_url(cedula)

