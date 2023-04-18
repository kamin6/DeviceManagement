from flask import Flask, render_template, request
from database import engine, load_members_from_db, load_devices_from_db
from midway import resp_info, response
from sqlalchemy import text
import http
import requests
import urllib.parse
from urllib.parse import urlparse
import logging
import http.cookiejar as cookielib
import re
import getpass
import os

app = Flask(__name__)

response_info = resp_info(response)

#The home route is defined below
@app.route("/")
def home():
  return render_template('home.html', tables=get_all_devices(), members=load_members_from_db(), count=0)

#The route for the devices page is defined with a parameter for the memberId
@app.route("/devices/<memberId>")
def devices(memberId):
  return render_template('devices.html', table=load_devices_from_db(memberId),
                          memberId=memberId)

#The route for deleting a device with the memberId and DeviceId parameters
@app.route("/devices/delete/<memberId>/<deviceId>")
def delete_device(memberId, deviceId):
  with engine.connect() as conn:
    query = conn.execute(
      text(f"""delete from devices where OWNER='{memberId}' and DEVICE_ID='{deviceId}'""")
    )
  return render_template('devices.html', table=load_devices_from_db(memberId),
                          memberId=memberId)

#The route for adding a device with only the memberId parameter and device data is read from the request 
@app.route("/devices/add/<memberId>")
def add_device(memberId):
  data = request.args

  with engine.connect() as conn:
    query = conn.execute(text(
      f"""INSERT INTO devices (DEVICE_ID, DEVICE_NAME, LOCATION, OWNER) VALUES ('{data["DEVICE_ID"]}', '{data["DEVICE_NAME"]}', '{data["LOCATION"]}', '{memberId}')"""
    ))

  return render_template('devices.html', table=load_devices_from_db(memberId),
                          memberId=memberId)

#The route for modifying existing device data
@app.route("/devices/edit/<memberId>/<deviceId>")
def edit_device(memberId, deviceId):
  data = request.args
  with engine.connect() as conn:
    query = conn.execute(
      text(f"""UPDATE devices SET DEVICE_ID='{data["DEVICE_ID"]}', DEVICE_NAME='{data["DEVICE_NAME"]}', LOCATION='{data["LOCATION"]}' where OWNER='{memberId}' and DEVICE_ID='{deviceId}'""")
    )
  return render_template('devices.html', table=load_devices_from_db(memberId),
                          memberId=memberId)

#The route for admin view that displays all device data for each member
@app.route("/devices/admin")
def admin_devices_view():
  # Add check for response from midway contains admin user ID
  return render_template('admin_page.html', tables=get_all_devices())

#Method that fetched all devices for each member and returns a 2 dimensional list
def get_all_devices():
  list_of_members = load_members_from_db()
  list_of_tables = []
  for member in list_of_members:
    list_of_tables.append(load_devices_from_db(member))
  return list_of_tables

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
