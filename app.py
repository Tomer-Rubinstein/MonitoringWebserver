from flask import Flask, render_template, request, jsonify, Response
from DB_Utils import *

from datetime import datetime
from dateutil import parser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

isAuthed = False # TODO: create authentication and authorization instead of this global var

@app.route("/", methods=["GET"])
def homepage():
  return render_template("pages/Homepage.html") # was: pages/DashboardPage.html

@app.route("/", methods=["POST", "GET"])
def homepage_post():
  global isAuthed
  username = request.form['username']
  password = request.form['password']

  if username == "root" and password == "toor":
    isAuthed = True
    return render_template("pages/DashboardPage.html")
  
  return render_template("pages/Homepage.html", error=True)


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


@app.route("/getData", methods=["GET"])
def getDataEndpoint():
  global isAuthed
  if not isAuthed:
    return "Sorry, you seem to have no permission to visit this page :("

  clients = [(i.user, i.cpuType, i.cpuUsage, i.memory, i.procs, i.timestamp, i.id) for i in Client.query.all()]

  for client in clients:
    if(client[5] != None and (datetime.now()-parser.parse(client[5])).seconds >= 7):
      clients.remove(client)                            # remove from the return value
      db.session.query(Client).filter_by(id=client[6]).delete() # remove from the database

  return jsonify(clients=clients)

if __name__ == "__main__":
  db.init_app(app)
  app.run(debug=True, threaded=True)
