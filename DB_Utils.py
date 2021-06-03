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
  ram = db.Column(db.String(20))

  """
    If client doesn't exists, create a new field.
    If it does, update the right field.
  """
  def addClient(self):

    c = Client(
      user=self.user, 
      cpuType=self.cpuType,
      cpuUsage=self.cpuUsage,
      memory=self.memory,
      procs=self.procs,
      ram=self.ram
    )
    db.session.add(c)
    db.session.commit()

  def __repr__(self):
    return f"Client({self.id}, {self.user}, {self.cpuType})"
