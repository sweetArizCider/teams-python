from object import Object

class Player(Object):
  def __init__(
    self, 
    name = None, 
    age = None,  
    number = None, #optional
    nationality = None, #optional
    position = None #optional
  ):
    is_array = (name is None and age is None)
    super().__init__(is_array=is_array)

    if not self.is_array:
      if name is None or age is None:
        raise ValueError("Both 'name' and 'age' are required for a Player.")
      self.name = name
      self.age = age
      self.number = number
      self.nationality = nationality
      self.position = position

  def __str__(self):
    if self.is_array:
      return super().__str__()
    return f"- Player: {self.name}, Age: {self.age}, Number: {self.number} , Nationality: {self.nationality}, Position: {self.position}"
    
if __name__ == '__main__':
  print("=================SINGLE PLAYER=================")
  single_player = Player('Carlos', 21)
  single_player2 = Player('Pamela', 19, 16, 'Mexico', 'Goalkeeper')
  single_player3 = Player('Jose', 32, 2, 'Mexico', 'Defensor')
  single_player4 = Player('Luis', 45, 76)

  print("=================PLAYERS ARRAY=================")
  players_array = Player()
  players_array.add(single_player)
  players_array.add(single_player2)
  players_array.add(single_player3)
  players_array.add(single_player4)


  # updates Jose to Ana
  players_array.update(index=3, object_element=Player('Ana', 29, 10, 'Spain', 'Midfielder'))
  # removes Luis
  players_array.remove(index=2)
  players_array.list()
  print(players_array)
  print("=================PLAYERS ARRAY=================")
  print(players_array.dictionary())
  print(single_player.dictionary())

  

  
