
class Player:
  def __init__(self, name: str, age: int, active: bool = True):
    self.name = name
    self.age = age
    self.active = active

  def change_name(self, new_name: str):
    if not new_name:
      return
    self.name = new_name

  def change_age(self, new_age: int):
    if not new_age:
      return
    self.age = new_age

  def desactive(self):
    self.active = False

  def activate(self):
    self.active = True

