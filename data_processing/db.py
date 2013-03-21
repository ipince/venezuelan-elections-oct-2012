#!/usr/bin/python

import MySQLdb as mdb
# TODO(ipince): comment

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
      source(
        id int auto_increment primary key,
        name varchar(20) not null
      );
      ''')
    self.cursor.execute('''
      create table if not exists
      center(
        id int not null auto_increment,
        rep_code int not null,
        primary key (id)
      );
    ''')
    self.cursor.execute('''
      create table if not exists
      person(
        cedula int not null,
        source_id int not null,
        full_name varchar(200),
        first_name varchar(50),
        second_name varchar(50),
        first_surname varchar(50),
        second_surname varchar(50),
        birthday int unsigned,
        primary key (cedula, source_id),
        foreign key (source_id) references source(id),
        index (cedula),
        index (first_name),
        index (first_surname)
      );
      ''')

  def save_person(self, cedula, source, full_name = None,
                  first_name = None, second_name = None,
                  first_surname = None, second_surname = None, birthday = None):
    self.cursor.execute('''
      insert into people(
        cedula, source, full_name, first_name, second_name, first_surname, second_surname, birthday)
      values (%s, %s, %s, %s, %s, %s, %s, %s)''',
      (cedula, source, full_name, first_name, second_name, first_surname, second_surname, birthday))
