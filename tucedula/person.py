#!/usr/bin/python

from google.appengine.ext import db

class Person(db.Model):
  cedula = db.StringProperty()
  full_name = db.StringProperty()
  first_name = db.StringProperty()
  second_name = db.StringProperty()
  first_surname = db.StringProperty()
  second_surname = db.StringProperty()
  #voting_center = VotingCenter()

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return str([(k, v) for (k, v) in self.__dict__.iteritems()])

class VotingCenter(object):
  def __init__(self):
    self.state = None
    self.municipality = None
    self.parish = None
    self.center = None
    self.address = None

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return str([(k, v) for (k, v) in self.__dict__.iteritems()])
