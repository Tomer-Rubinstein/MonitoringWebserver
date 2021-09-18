from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

# TODO: When the client disconnects from the webserver, delete him from the db.
# ^ solution: do it in the frontend, if no update in 15 seconds, remove from db.

class Client(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.String(20), nullable=False)
  cpuType = db.Column(db.String(30), nullable=False)
  cpuUsage = db.Column(db.String(5), nullable=False)
  memory = db.Column(db.String(20), nullable=False)
  procs = db.Column(db.String(200))

  def addClient(self):
    # Update values for user if the user exists on the db
    if Client.query.filter_by(user=self.user).first() is not None:
      print(f"Not none: {self.cpuUsage} {self.memory} {self.user}")
      _user = Client.query.filter_by(user=self.user).first()
      _user.cpuUsage = self.cpuUsage
      _user.memory = self.memory
      _user.procs = self.procs
      db.session.commit()
      return
    
    c = Client(
      user=self.user, 
      cpuType=self.cpuType,
      cpuUsage=self.cpuUsage,
      memory=self.memory,
      procs=self.procs,
    )
    db.session.add(c)
    db.session.commit()

  def __repr__(self):
    return f"Client({self.id}, {self.user}, {self.cpuUsage}, {self.memory})"
