from flask import Flask, render_template, request, jsonify, Response
from DB_Utils import Client

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


@app.route("/", methods=["GET"])
def homepage():
  return render_template("pages/DashboardPage.html") # was: pages/Homepage.html

@app.route("/", methods=["POST", "GET"])
def homepage_post():
  username = request.form['username']
  password = request.form['password']
  if username == "root" and password == "toor":
    return render_template("pages/DashboardPage.html")
  return render_template("pages/Homepage.html", error=True)

# TODO: Create a function to handle API calls and store the info at
# the clients dictionary.
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
    ram=ram
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

if __name__ == "__main__":
  app.run(debug=True, threaded=True)
