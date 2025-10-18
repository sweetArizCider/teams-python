from object import Object

class Team(Object):
  def __init__(
      self,
      name=None,
      sport=None,
      city=None  # optional, default is None
  ):
    is_array = (name is None and sport is None)
    super().__init__(is_array=is_array)

    if not self.is_array:
      if name is None or sport is None:
        raise ValueError("Both 'name' and 'sport' are required for a Team.")
      self.name = name
      self.sport = sport
      self.city = city

  def __str__(self):
    if self.is_array:
      return super().__str__()
    return f"- Team: {self.name}, Sport: {self.sport}, City: {self.city}"

if __name__ == '__main__':
  print('hello')