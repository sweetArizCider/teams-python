class Object:
  def __init__(self):
    self.is_array = True
    self.object_array = []

  def list(self):
    if not self.is_array:
      return print("This is not an Array!")
    for object_element in self.object_array:
      print(f"\n{object_element}")
    return None
  
  def add(self, object_element):
    if not self.is_array:
      return print("This is not an Array of teams!, team not added")
    self.object_array.append(object_element)
    return print("Object added!")

  def update(self, index, object_element):
    if index is None:
      return print("Index is required!!")
    if not self.is_array:
      return print("This is not an array!!")
    if not object_element:
      return print("Object is required!")
    self.object_array[index] = object_element
    return print("Object updated!")

  def remove(self, index):
    if index is None:
      return print("Index is required!!")
    if not self.is_array:
      return print("This is not an array of teams!!")
    self.object_array.pop(index)
    return print("Team removed!")
  