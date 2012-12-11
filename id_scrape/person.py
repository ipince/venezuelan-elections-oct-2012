#!/usr/bin/python

class Person(object):
  def __init__(self):
    self.cedula = None
    self.full_name = None
    self.first_name = None
    self.second_name = None
    self.first_surname = None
    self.second_surname = None
    self.voting_center = VotingCenter()

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
