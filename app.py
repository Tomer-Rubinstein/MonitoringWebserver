from flask import Flask, render_template, request, jsonify, Response
from DB_Utils import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # TODO: In production, change to a postgres db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

isAuthed = False # WARNING: global variables are not allowed!

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
  ram = request.form.get('ram')
  memory = ram
  user = request.form.get('username')
  cpuUsage = request.form.get('cpuUsage')
  procs = request.form.get('processes')

  print(cpuType, ram, user, cpuUsage, memory, procs)

  client = Client(
    user=user, 
    cpuType=cpuType,
    cpuUsage=cpuUsage,
    memory=memory,
    procs=procs,
  )
  client.addClient()

  Client.query.all()
  return jsonify({
    "cpuType": cpuType,
    "ram": ram,
    "user": user,
    "cpuUsage": cpuUsage,
    "memory": memory,
    "processes": procs,
  })


@app.route("/getData", methods=["GET"])
def getDataEndpoint():
  global isAuthed
  if not isAuthed:
    return "Sorry, you seem to have no permission to visit this page :("

  clients = [(i.user, i.cpuType, i.cpuUsage, i.memory, i.procs) for i in Client.query.all()]
  return jsonify(clients=clients)

if __name__ == "__main__":
  db.init_app(app)
  app.run(debug=True, threaded=True)
