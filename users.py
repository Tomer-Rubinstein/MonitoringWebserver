
class User:
  def __init__(self, id, username, password) -> None:
    self.id = id
    self.username = username
    self.password = password


users = [
  User(1, "root", "toor")
]

users_table = {u.username: u for u in users}
users_id    = {u.id: u for u in users}
