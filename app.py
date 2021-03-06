from logging import error
from flask import Flask, render_template, request, jsonify, Response, redirect
from flask_jwt import jwt_required
from DB_Utils import *

from datetime import datetime
from dateutil import parser

from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

import requests
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ['USERNAME']


"""
  if username exists and password matches, return the user object
  params:
    - username(string), the user to log in to
    - password(string), used to check if the request has authorization to login to that user
"""
def authenticate(username, password):
  print(username, password)
  user = users_table.get(username, None) # using a dictionary for easier lookup
  if user and safe_str_cmp(password.encode("utf-8"), user.password.encode("utf-8")):
    return user
  return None


"""
 return user object by his ID
 params:
   - payload: the jwt token
"""
def identity(payload):
  id = payload['identity']
  return users_id.get(id, None)


jwt = JWT(app, authenticate, identity)


@app.route("/", methods=["GET", "POST"])
def homepage():
  return render_template("pages/Homepage.html")

@app.route("/register")
def regiter():
  return render_template("pages/RegistrationPage.html")

@app.route("/registerUser", methods=["POST"])
def registerUser():
  username = request.form.get("username")
  password = request.form.get("password")

  newUser = User(username=username, password=password)
  if newUser.addUser() == 1:
    errorLog = f"Username \"{username}\" already exists"
    return jsonify(error=errorLog, status=208)

  return jsonify(status=201)


@app.route("/dashboard", methods=["POST"])
def dashboard():
  username = request.form.get("username")
  password = request.form.get("password")
  dest = request.host_url + "auth"

  r = requests.post(dest, json={"username": username, "password": password})

  if r.status_code == 401:
    return redirect(request.host_url, code=303)

  token = "JWT " + r.json().get("access_token")

  dest = request.host_url + "panelContent"
  r = requests.get(dest, headers={"Authorization": token})

  return r.text


@app.route("/panelContent")
@jwt_required()
def panelContent():
  return render_template("pages/DashboardPage.html", token=request.headers.get("Authorization"))
  


@app.route("/getData", methods=["GET"])
@jwt_required()
def getDataEndpoint():
  clients = [(i.user, i.cpuType, i.cpuUsage, i.memory, i.procs, i.timestamp, i.id) for i in Client.query.all()]

  for client in clients:
    if(client[5] != None and (datetime.now()-parser.parse(client[5])).seconds >= 7):
      clients.remove(client)                                    # remove from the return value
      db.session.query(Client).filter_by(id=client[6]).delete() # remove from the database
      db.session.commit()

  return jsonify(clients=clients)



@app.route("/api", methods=["POST"])
def api():
  cpuType = request.form.get('cpuType')
  memory = request.form.get('ram')
  user = request.form.get('username')
  cpuUsage = request.form.get('cpuUsage')
  procs = request.form.get('processes')
  timestamp = str(datetime.now())

  print("\t", cpuType, user, cpuUsage, memory, procs, timestamp)

  client = Client(
    user=user, 
    cpuType=cpuType,
    cpuUsage=cpuUsage,
    memory=memory,
    procs=procs,
    timestamp=timestamp
  )
  client.addClient()

  return jsonify({
    "cpuType": cpuType,
    "user": user,
    "cpuUsage": cpuUsage,
    "memory": memory,
    "processes": procs,
    "timestamp": timestamp,
  })



if __name__ == "__main__":
  db.init_app(app)
  app.run(debug=True, threaded=True)
