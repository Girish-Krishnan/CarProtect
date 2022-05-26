import json
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response, FileResponse

from datetime import datetime

import mysql.connector as mysql
import os.path
import base64
import datetime
from os.path import isfile, join
from mimetypes import MimeTypes
from os import listdir
import wand
from wand.image import Image
import hashlib
import shutil
import json
import time
import hmac
import copy
import sys
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


def upload_image(request):
  try:
    response = Image.upload(PyramidAdapter(request), "/public/")
  except Exception:
    response = {"error": str(sys.exc_info()[1])}
  return Response(json.dumps(response))


def upload_image_validation(request):

  def validation(filePath, mimetype):
    with wand.image.Image(filename = filePath) as img:
      if img.width != img.height:
        return False
      return True

  options = {
  "fieldname": "myImage",
  "validation": validation
  }

  try:
    response = Image.upload(PyramidAdapter(request), "/public/", options)
  except Exception:
    response = {"error": str(sys.exc_info()[1])}
  return Response(json.dumps(response))


class Image(object):

  defaultUploadOptions = {
"fieldname": "file",
"validation": {
 "allowedExts": ["gif", "jpeg", "jpg", "png", "svg", "blob"],
 "allowedMimeTypes": ["image/gif", "image/jpeg", "image/pjpeg", "image/x-png", "image/png",
                      "image/svg+xml"]
},
# string resize param from http://docs.wand-py.org/en/0.4.3/guide/resizecrop.html#transform-images
# Examples: "100x100", "100x100!". Find more on http://www.imagemagick.org/script/command-line-processing.php#geometry
"resize": None
}

  @staticmethod
  def upload(req, fileRoute, options = None):
    """
Image upload to disk.
Parameters:
 req: framework adapter to http request. See BaseAdapter.
 fileRoute: string
 options: dict optional, see defaultUploadOptions attribute
Return:
 dict: {link: "linkPath"}
"""
    if options is None:
      options = Image.defaultUploadOptions
    else:
      options = Utils.merge_dicts(Image.defaultUploadOptions, options)

    return File.upload(req, fileRoute, options)

  @staticmethod
  def delete(src):
    """
Delete image from disk.
Parameters:
 src: string
"""
    return File.delete(src)

  @staticmethod
  def list(folderPath, thumbPath = None):
    """
List images from disk.
Parameters:
 folderPath: string
 thumbPath: string
Return:
 list: list of images dicts. example: [{url: "url", thumb: "thumb", name: "name"}, ...]
"""

    if thumbPath == None:
      thumbPath = folderPath

# Array of image objects to return.
    response = []

    absoluteFolderPath = Utils.getServerPath() + folderPath

# Image types.
    imageTypes = Image.defaultUploadOptions["validation"]["allowedMimeTypes"]

# Filenames in the uploads folder.
    fnames = [f for f in listdir(absoluteFolderPath) if isfile(join(absoluteFolderPath, f))]

    for fname in fnames:
      mime = MimeTypes()
      mimeType = mime.guess_type(absoluteFolderPath + fname)[0]

      if mimeType in imageTypes:
        response.append({
         "url": folderPath + fname,
         "thumb": thumbPath + fname,
         "name": fname
     })

    return response


class Utils(object):
  """
Utils static class.
"""

  @staticmethod
  def hmac(key, string, hex = False):
    """
Calculate hmac.
Parameters:
 key: string
 string: string
 hex: boolean optional, return in hex, else return in binary
Return:
 string: hmax in hex or binary
"""

# python 2-3 compatible:
    try:
      hmac256 = hmac.new(key.encode() if isinstance(key, str) else key, msg = string.encode("utf-8") if isinstance(string, str) else string, digestmod = hashlib.sha256) # v3
    except Exception:
      hmac256 = hmac.new(key, msg = string, digestmod = hashlib.sha256) # v2

    return hmac256.hexdigest() if hex else hmac256.digest()

  @staticmethod
  def merge_dicts(a, b, path = None):
    """
Deep merge two dicts without modifying them. Source: http://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/7205107#7205107
Parameters:
 a: dict
 b: dict
 path: list
Return:
 dict: Deep merged dict.
"""

    aClone = copy.deepcopy(a);
# Returns deep b into a without affecting the sources.
    if path is None: path = []
    for key in b:
      if key in a:
        if isinstance(a[key], dict) and isinstance(b[key], dict):
         aClone[key] = Utils.merge_dicts(a[key], b[key], path + [str(key)])
        else:
         aClone[key] = b[key]
      else:
        aClone[key] = b[key]
    return aClone

  @staticmethod
  def getExtension(filename):
    """
Get filename extension.
Parameters:
 filename: string
Return:
 string: The extension without the dot.
"""
    return os.path.splitext(filename)[1][1:]

  @staticmethod
  def getServerPath():
    """
Get the path where the server has started.
Return:
 string: serverPath
"""
    return os.path.abspath(os.path.dirname(sys.argv[0]))

  @staticmethod
  def isFileValid(filename, mimetype, allowedExts, allowedMimeTypes):
    """
Test if a file is valid based on its extension and mime type.
Parameters:
 filename string
 mimeType string
 allowedExts list
 allowedMimeTypes list
Return:
 boolean
"""

# Skip if the allowed extensions or mime types are missing.
    if not allowedExts or not allowedMimeTypes:
      return False

    extension = Utils.getExtension(filename)
    return extension.lower() in allowedExts and mimetype in allowedMimeTypes

  @staticmethod
  def isValid(validation, filePath, mimetype):
    """
Generic file validation.
Parameters:
 validation: dict or function
 filePath: string
 mimetype: string
"""

# No validation means you dont want to validate, so return affirmative.
    if not validation:
      return True

# Validation is a function provided by the user.
    if callable(validation):
      return validation(filePath, mimetype)

    if isinstance(validation, dict):
      return Utils.isFileValid(filePath, mimetype, validation["allowedExts"], validation["allowedMimeTypes"])

# Else: no specific validating behaviour found.
    return False


class BaseAdapter(object):
  """
Interface. Inherit this class to use the lib in your framework.
"""

def __init__(self, request):
  """
Constructor.
Parameters:
 request: http request object from some framework.
"""
  self.request = request

def riseError(self):
  """
Use this when you want to make an abstract method.
"""
  raise NotImplementedError( "Should have implemented this method." )

def getFilename(self, fieldname):
  """
Get upload filename based on the fieldname.
Parameters:
 fieldname: string
Return:
 string: filename
"""
  self.riseError()

def getMimetype(self, fieldname):
  """
Get upload file mime type based on the fieldname.
Parameters:
 fieldname: string
Return:
 string: mimetype
"""
  self.riseError()

def saveFile(self, fieldname, fullNamePath):
  """
Save the upload file based on the fieldname on the fullNamePath location.
Parameters:
 fieldname: string
 fullNamePath: string
"""
  self.riseError()


class PyramidAdapter(BaseAdapter): 
  """
Pyramid Adapter: Check BaseAdapter to see what methods description.
"""

def checkFile(self, fieldname):
  if fieldname not in self.request.POST:
    raise Exception("File does not exist.")

def getFilename(self, fieldname):
  self.checkFile(fieldname)
  return self.request.POST[fieldname].filename

def getMimetype(self, fieldname):
  self.checkFile(fieldname)
  return self.request.POST[fieldname].type

def saveFile(self, fieldname, fullNamePath):
  self.checkFile(fieldname)
  file = self.request.POST[fieldname].file

  file.seek(0)
  with open(fullNamePath, "wb") as output_file:
    shutil.copyfileobj(file, output_file)

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

  config.add_route("upload_image", "/upload_image")
  config.add_view(upload_image, route_name = "upload_image")

  config.add_route("upload_image_validation", "/upload_image_validation")
  config.add_view(upload_image_validation, route_name = "upload_image_validation")


  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()
