import json
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response

from datetime import datetime

import mysql.connector as mysql
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

def get_home(req):
  # Connect to the database and retrieve the users
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select first_name, last_name, email, focus from Users;")
  records = cursor.fetchall()
  db.close()

  return render_to_response('templates/home.html', {'users': records}, request=req)

def get_unlock(req):
  name = req.matchdict['username']
  code = req.matchdict['password']

  # Connect to the database and retrieve the users

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select * from Login_Data where username = %s and password = %s;", (name, code))

  if cursor.fetchone() is not None:

    return {'username': name,
              'password':code
      }
  else:
    return {'username': '',
              'password':''
      }

def send_data(req):
  username = req.matchdict['username']
  password = req.matchdict['password']
  pir = req.matchdict['pir']
  vib = req.matchdict['vib']
  ax = req.matchdict['ax']
  ay = req.matchdict['ay']
  az = req.matchdict['az']
  lat = req.matchdict['lat']
  long = req.matchdict['long']

  # Connect to the database and retrieve the users
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("insert into Sensor_Data (username, password, pir, vib, ax, ay, az, latitude, longitude, time_added) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (username, password, pir, vib, ax, ay, az, lat, long, str(datetime.now())))
  db.commit()
  db.close()
  return {}

def stream_data(req):
  username = req.matchdict['username']
  password = req.matchdict['password']
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select pir,vib,ax,ay,az,latitude,longitude from Sensor_Data where username = %s and password = %s order by time_added DESC;", (username, password))
  records = cursor.fetchone()
  db.close()
  return {
    'pir': records[0],
    'vib': records[1],
    'ax': records[2],
    'ay': records[3],
    'az': records[4],
    'lat': records[5],
    'long': records[6]
  }

''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('get_home', '/')
  config.add_view(get_home, route_name='get_home')

  config.add_route('unlock', '/unlock/{username}/{password}/')
  config.add_view(get_unlock, route_name='unlock',renderer='json')

  config.add_route('send_data', '/send_data/{username}/{password}/{pir}/{vib}/{ax}/{ay}/{az}/{lat}/{long}/')
  config.add_view(send_data, route_name='send_data',renderer='json')

  config.add_route('stream_data', '/stream_data/{username}/{password}/')
  config.add_view(stream_data, route_name='stream_data',renderer='json')

  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()
