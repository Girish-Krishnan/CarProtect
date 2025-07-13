from pyramid.renderers import render_to_response
from pyramid.response import Response
from datetime import datetime
import uuid
import os
import shutil
import numpy as np
import cv2
from PIL import Image

from .db import get_connection


def get_home(request):
    """Render the landing page showing users."""
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("select first_name, last_name, email, focus from Users;")
    records = cursor.fetchall()
    db.close()
    return render_to_response('templates/home.html', {'users': records}, request=request)


def get_unlock(request):
    """Verify username and password."""
    name = request.matchdict['username']
    code = request.matchdict['password']
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "select * from Login_Data where username = %s and password = %s;",
        (name, code)
    )
    if cursor.fetchone() is not None:
        return {'username': name, 'password': code}
    return {'username': '', 'password': ''}


def send_data(request):
    """Store sensor readings from ESP32."""
    data = request.matchdict
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "insert into Sensor_Data (username, password, pir, vib, ax, ay, az, latitude, longitude, time_added) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
        (
            data['username'], data['password'], data['pir'], data['vib'],
            data['ax'], data['ay'], data['az'], data['lat'], data['long'],
            str(datetime.now())
        )
    )
    db.commit()
    db.close()
    return {}


def stream_data(request):
    """Return the latest sensor data for a user."""
    username = request.matchdict['username']
    password = request.matchdict['password']
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        "select pir, vib, ax, ay, az, latitude, longitude from Sensor_Data "
        "where username = %s and password = %s order by time_added DESC;",
        (username, password)
    )
    records = cursor.fetchone()
    db.close()
    if records:
        return {
            'pir': records[0],
            'vib': records[1],
            'ax': records[2],
            'ay': records[3],
            'az': records[4],
            'lat': records[5],
            'long': records[6],
        }
    return {}


def store_image(request):
    """Store an uploaded image from the camera."""
    filename = request.POST['imageFile'].filename
    input_file = request.POST['imageFile'].file
    image = Image.open(input_file)
    img_array = np.array(image)
    cv2.imwrite(
        "public/image.jpg",
        cv2.rotate(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB), cv2.ROTATE_180)
    )
    file_path = os.path.join('/tmp', f"{uuid.uuid4()}.jpg")
    temp_file = file_path + '~'
    input_file.seek(0)
    with open(temp_file, 'wb') as output_file:
        shutil.copyfileobj(input_file, output_file)
    os.rename(temp_file, file_path)
    return Response('OK')
