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
  #print "\tExtracted links: " + str(links)
  return links

def extract_candidate_votes(tree):
  votes = {}
  for tr in tree.xpath('//tr[@class="tbsubtotalrow"]'):
    cells = tr.xpath('td[@class="lightRowContent"]/span')
    votes[cells[0][0].text] = str(cells[1].text).replace('.', '')
  print "\tExtracted candidate votes: " + str(votes)
  return votes

def extract_total_votes(tree):
  totals = {}
  for row in tree.xpath('//div[@id="fichaTecnica"]//tr[@class="tblightrow"]'):
    keys = row.xpath('td/span/b')
    values = row.xpath('td[last()]')
    for i in range(len(keys)):
      if (values[i].text):
        totals[keys[i].text] = str(values[i].text).replace('.', '')
  print "\tExtracted totals: " + str(totals)
  return totals

def extract_votes(tree):
  d1 = extract_candidate_votes(tree)
  d2 = extract_total_votes(tree)
  return dict(d1.items() + d2.items())

def write_to_file(votes):
  state_based = ''
  muni_based = ''
  parish_based = ''
  for state in votes:
    state_based += "\t".join([state] + votes[state]["total"].values()) + "\n"
    for muni in votes[state]:
      if muni == "total":
        continue
      muni_based += "\t".join([state, muni] + votes[state][muni]["total"].values()) + "\n"
      for (parish, values) in votes[state][muni].iteritems():
        if parish == "total":
          continue
        parish_based += "\t".join([state, muni, parish] + values.values()) + "\n"
  file('state.csv', 'w').write(state_based)
  file('muni.csv', 'w').write(muni_based)
  file('parish.csv', 'w').write(parish_based)

url_root = 'http://www.cne.gob.ve/resultado_presidencial_2012/r/1/';
country_url = url_root + 'reg_000000.html'

# votes is of the form:
#  {<State> -> {<Muni> -> {<Parish> -> {<Candidate> -> <votes>}}}}
votes = {}

state_links = extract_nav_links(parse(country_url))
for state_link in itertools.islice(state_links, 0, 1000):
  print "Processing STATE " + state_link
  state_tree = parse(url_root + state_links[state_link])
  muni_links = extract_nav_links(state_tree)
  muni_dict = defaultdict(dict)
  # muni dict holds details per muni and state totals (which is muni-aggregated totals)
  muni_dict["total"] = extract_votes(state_tree)
  for muni_link in itertools.islice(muni_links, 0, 1000):
    print "Processing MUNI " + muni_link
    muni_tree = parse(url_root + muni_links[muni_link])
    parish_links = extract_nav_links(muni_tree)
    muni_dict[muni_link]["total"] = extract_votes(muni_tree)
    for parish_link in itertools.islice(parish_links, 0, 1000):
      print "Processing PARISH " + parish_link
      muni_dict[muni_link][parish_link] = extract_votes(parse(url_root + parish_links[parish_link]))
  votes[state_link] = muni_dict

write_to_file(votes)
