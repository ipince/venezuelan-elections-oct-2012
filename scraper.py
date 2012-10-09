#!/usr/bin/python

import os
import urllib2
import itertools
from collections import defaultdict
from lxml import etree


def cached_url(url):
  return os.path.join("cache", url.replace("/", "_").replace(":", "_"))

def parse(url):
  print "Fetching: " + url
  cached = cached_url(url)
  contents = ""
  if os.path.exists(cached):
    print "Reading from cached file %s" % cached
    contents = file(cached).read()
  else:
    contents = urllib2.urlopen(url).read()
    outfile = file(cached, 'w')
    outfile.write(contents)
  return etree.HTML(contents)

def extract_nav_links(tree):
  BAD_LINKS = ['EMBAJADA', 'INHOSPITOS']
  links = {}
  for elem in tree.xpath('//li[@class="region-nav-item"]/a[@id="region_ref"]'):
    if (elem.text not in BAD_LINKS):
      links[elem.text] = elem.get("href")
  print "Extracted links: " + str(links)
  return links

def extract_candidate_votes(tree):
  votes = {}
  for tr in tree.xpath('//tr[@class="tbsubtotalrow"]'):
    cells = tr.xpath('td[@class="lightRowContent"]/span')
    votes[cells[0][0].text] = cells[1].text
  print votes
  return votes

def extract_total_votes(tree):
  totals = {}
  for row in tree.xpath('//div[@id="fichaTecnica"]//tr[@class="tblightrow"]'):
    keys = row.xpath('td/span/b')
    values = row.xpath('td[last()]')
    for i in range(len(keys)):
      if (values[i].text):
        totals[keys[i].text] = str(values[i].text).replace('.', '')
  print totals
  return totals

def write_to_file(votes):
  str = ''
  for state in votes:
    for muni in votes[state]:
      for (parish, values) in votes[state][muni].iteritems():
        str += "\t".join([state, muni, parish] + [v.replace(".", "") for v in values.values()]) + "\n"
  file('data22.csv', 'w').write(str)

url_root = 'http://www.cne.gob.ve/resultado_presidencial_2012/r/1/';
country_url = url_root + 'reg_000000.html'

# votes is of the form:
#  {<State> -> {<Muni> -> {<Parish> -> {<Candidate> -> <votes>}}}}
votes = {}

state_links = extract_nav_links(parse(country_url))
for state_link in itertools.islice(state_links, 0, 1000):
  muni_links = extract_nav_links(parse(url_root + state_links[state_link]))
  muni_dict = defaultdict(dict)
  for muni_link in itertools.islice(muni_links, 0, 1000):
    parish_links = extract_nav_links(parse(url_root + muni_links[muni_link]))
    parish_dict = {}
    for parish_link in itertools.islice(parish_links, 0, 1000):
      tree = parse(url_root + parish_links[parish_link])
      candidate_votes_by_parish = extract_candidate_votes(tree)
      total_votes_by_parish = extract_total_votes(tree)
      votes_by_parish = dict(candidate_votes_by_parish.items() + total_votes_by_parish.items())
      muni_dict[muni_link][parish_link] = votes_by_parish
  votes[state_link] = muni_dict

write_to_file(votes)
