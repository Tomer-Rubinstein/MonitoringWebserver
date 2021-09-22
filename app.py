from flask import Flask, render_template, request, jsonify, Response
from flask_jwt import jwt_required
from DB_Utils import *

from datetime import datetime
from dateutil import parser

from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from users import *

import requests

# refactor, review and document the code base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'gfjijk345jkfd,xz' # [TODO] create an environment variable


"""
  if username exists and password matches, return the user object
  params:
    - username(string), the user to log in to
    - password(string), used to check if the request has authorization to login to that user
"""
def authenticate(username, password) -> User:
  print(username, password)
  user = users_table.get(username, None) # using a dictionary for easier lookup
  if user and safe_str_cmp(password.encode("utf-8"), "toor"):
    return user
  return None


"""
 return user object by his ID
 params:
   - payload: the jwt token
"""
def identity(payload) -> User:
  id = payload['identity']
  return users_id.get(id, None)


jwt = JWT(app, authenticate, identity)


@app.route("/", methods=["GET", "POST"])
def homepage():
  return render_template("pages/Homepage.html")


@app.route("/dashboard", methods=["POST"])
def sendLoginInfo():
  username = request.form.get("username")
  password = request.form.get("password")
  dest = request.host_url + "auth"

  r = requests.post(dest, json={"username": username, "password": password})
  token = "JWT " + r.json()["access_token"]

  dest = request.host_url + "login"
  r = requests.get(dest, headers={"Authorization": token})

  return r.text


@app.route("/login")
@jwt_required()
def dashboard():
  return render_template("pages/DashboardPage.html", token=request.headers.get("Authorization"))
  


@app.route("/getData")
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

  if cpuUsage == "0.0":
    cpuUsage = "Calculating..."
  else:
    cpuUsage += "%"


  client = Client(
    user=user, 
    cpuType=cpuType,
    cpuUsage=cpuUsage,
    memory=memory,
    procs=procs,
    timestamp=timestamp
  )
  client.addClient()
  Client.query.all()

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
