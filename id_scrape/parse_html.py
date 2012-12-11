#!/usr/bin/python

import codecs
import os
import person as p
import time

from lxml import etree
from lxml.html.soupparser import fromstring

def parse_html(filename):
  contents = file(filename).read()
  # Characte set is not included in file html contents, so work with unicode objs instead
  contents = codecs.decode(contents, 'utf-8')
  return etree.HTML(contents)

def extract_data(tree):
  person = p.Person()
  for elem in tree.xpath('/html/body/table/tr/td/table/tr[5]/td/table[1]/tr[2]/td/table/tr'):
    text = etree.tostring(elem, method="text", encoding="unicode")
    text = text.replace('\n', '').replace('\t', '').lower()
    pairs = text.split(':', 1)
    if (len(pairs) < 2):
      # TODO: check if voted on dec 16 and/or oct7
      text
    else: # two elements in pairs list
      if (pairs[0] == u'c\xe9dula'):
        person.cedula = pairs[1].replace('v-', '')
      elif (pairs[0] == u'nombre'):
        person.full_name = pairs[1]
      elif (pairs[0] == u'nombres'):
        names = pairs[1].split()
        if (len(names) == 4):
          person.first_name = names[0]
          person.second_name = names[1]
          person.first_surname = names[2]
          person.second_surname = names[3]
      elif (pairs[0] == u'estado'):
        person.voting_center.state = pairs[1]
      elif (pairs[0] == u'municipio'):
        person.voting_center.municipality = pairs[1]
      elif (pairs[0] == u'parroquia'):
        person.voting_center.parish = pairs[1]
      elif (pairs[0] == u'centro'):
        person.voting_center.center = pairs[1]
      elif (pairs[0] == u'direcci\xf3n'):
        person.voting_center.address = pairs[1]
  print person
  return person

count = 0 
cache_dir = 'cache/07/000'
for filename in sorted(os.listdir(cache_dir)):
  print filename
  full_filename = os.path.join(cache_dir, filename)
  print "mtime %s" % time.ctime(os.path.getmtime(full_filename))
  print "ctime %s" % time.ctime(os.path.getctime(full_filename))
  tree = parse_html(full_filename)
  extract_data(tree)
  count += 1
  if (count > 1): break

