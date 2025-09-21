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
    is_object_array = isinstance(object_array, list)

    if is_object_array:
      result = []
      for object in object_array:
        if hasattr(object, "dictionary") and callable(object.dictionary):
          result.append(object.dictionary())
        elif hasattr(object, "__dict__"):
          fields_dict = {
            field_name: field_value
            for field_name, field_value in object.__dict__.items()
            if field_name not in ("is_array", "object_array")
          }
          result.append(fields_dict)
        else:
          result.append({"value": str(object)})
      return result

    if hasattr(self, "__dict__"):
      return {k: v for k, v in self.__dict__.items() if k not in ("is_array", "object_array")}
    return {"value": str(self)}
  