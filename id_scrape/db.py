#!/usr/bin/python

import MySQLdb as mdb

class DB(object):
  def __init__(self, dbname):
    self.conn = mdb.connect('localhost', 'vene', 'venepass', dbname)
    self.cursor = self.conn.cursor()

  def get_version(self):
    self.cursor.execute('SELECT VERSION()')
    return self.cursor.fetchone()

  def create_tables(self):
    self.cursor.execute('''
      create table if not exists
      venezuelans(
        id int primary key auto_increment,
        cedula int unsigned not null,
        full_name varchar(200),
        first_name varchar(50),
        second_name varchar(50),
        first_surname varchar(50),
        second_surname varchar(50),
        index (cedula),
        index (first_name),
        index (first_surname)
      );
      ''')

  def save_person(self, cedula, full_name = None,
                  first_name = None, second_name = None,
                  first_surname = None, second_surname = None):
    self.cursor.execute('''
      insert into venezuelans(
        cedula, full_name, first_name, second_name, first_surname, second_surname)
      values (%s, %s, %s, %s, %s, %s)''',
      (cedula, full_name, first_name, second_name, first_surname, second_surname))
