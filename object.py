class Object:
  def __init__(self):
    self.is_array = True
    self.object_array = []

  def list(self):
    if not self.is_array:
      return print("This is not an Array!")
    for object in self.object_array:
      print(f"\n{object}")
    return
  
  def add(self, object):
    if not self.is_array:
      return print("This is not an Array of teams!, team not added")
    team.index = len(self.teams)
    self.teams.append(team)
    return print("Team added!")

  def update(self, index, object):
    if index == None:
      return print("Index is required!!")
    if not self.is_array:
      return print("This is not an array of teams!!")
    if not object:
      return print("Object is required!")
    self.object_array[index] = object
    return print("Object updated!")

  def remove(self, index):
    if index == None:
      return print("Index is required!!")
    if not self.is_array:
      return print("This is not an array of teams!!")
    self.teams.pop(index)
    return print("Team removed!")
  