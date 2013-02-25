#!/usr/bin/python

import webapp2
import logging
import person
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):

  def get(self):
    logging.info("This is some log")
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render({}))

  def post(self):
    p = person.Person(key_name=self.request.get("cedula"),
                      cedula=self.request.get("cedula"),
                      first_name=self.request.get("first_name"))
    p.put()

app = webapp2.WSGIApplication([('/', MainPage), ('/cedula/insert', MainPage)],
                              debug=True)

