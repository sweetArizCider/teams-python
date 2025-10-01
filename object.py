class Object:
  def __init__(self, is_array=True):
      self.is_array = is_array
      self.object_array = [] if is_array else None

  def __str__(self):
      if self.is_array:
          count = len(self.object_array)
          return f"There's {count} objects in the array." if count > 0 else "This is an empty array."
      return "This is a single object."

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

  def dictionary(self):
    object_array = getattr(self, "object_array", None)
    excluded_properties = {"is_array", "object_array"}

    if isinstance(object_array, list):
      return [object.dictionary() for object in object_array]

    if hasattr(self, "__dict__"):
      return {
        object_property_key: object_property_value
        for object_property_key, object_property_value in self.__dict__.items()
        if object_property_key not in excluded_properties
      }
    return None






