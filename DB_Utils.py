from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Client(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.String(20), nullable=False)
  cpuType = db.Column(db.String(30), nullable=False)
  cpuUsage = db.Column(db.String(5), nullable=False)
  memory = db.Column(db.String(20), nullable=False)
  procs = db.Column(db.String(200))
  timestamp = db.Column(db.String(70))

  def addClient(self):
    # Update values for user if the user exists on the db
    if Client.query.filter_by(user=self.user).first() is not None:
      _user = Client.query.filter_by(user=self.user).first()
      _user.cpuUsage = self.cpuUsage
      _user.memory = self.memory
      _user.procs = self.procs
      _user.timestamp = self.timestamp
      _user.user = self.user
      _user.cpuType = self.cpuType
      db.session.commit()
      return
    
    c = Client(
      user=self.user,
      cpuType=self.cpuType,
      cpuUsage=self.cpuUsage,
      memory=self.memory,
      procs=self.procs,
      timestamp=self.timestamp
    )
    db.session.add(c)
    db.session.commit()

  def __repr__(self):
    return f"Client({self.id}, {self.user}, {self.cpuUsage}, {self.memory})"


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), nullable=False)
  password = db.Column(db.String(25), nullable=False)

  def addUser(self):
    # Update values for user if the user exists on the db
    if User.query.filter_by(username=self.username).first() is not None:
      return 1
    
    u = User(
      username=self.username,
      password=self.password
    )
    db.session.add(u)
    db.session.commit()
    return 0


users = [u for u in User.query.all()]

users_table = {u.username: u for u in users}
users_id    = {u.id: u for u in users}
