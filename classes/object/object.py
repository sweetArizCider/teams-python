import json

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

  def to_json_file(self, filename):
    object_array = getattr(self, "object_array", None)
    excluded_properties = {"is_array", "object_array"}

    if isinstance(object_array, list):
      json_data = [object.dictionary() for object in object_array]
    elif hasattr(self, "__dict__"):
      json_data = {
        object_property_key: object_property_value
        for object_property_key, object_property_value in self.__dict__.items()
        if object_property_key not in excluded_properties
      }
    else:
      json_data = None

    if json_data is not None:
      with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=2)
      print(f"Object saved to {filename}")
    else:
      print("No data to save")


  def json_to_object(self, json_file):
    with open(json_file, 'r', encoding='utf-8') as json_file_data:
      data = json.load(json_file_data)

    if isinstance(data, list):
      object_array_instance = self.__class__()
      for item in data:
        temporal_object = self.__class__(**item)
        object_array_instance.add(temporal_object)
      return object_array_instance
    return self.__class__(**data)






