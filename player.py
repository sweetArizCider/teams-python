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
    if not (name is None or age is None):
      self.name = name
      self.age = age
      self.number = number if number is not None else None
      self.nationality = nationality if nationality is not None else None
      self.position = position if position is not None else None
    else:
      super().__init__()

  # TODO COMPLETE THE EXTENTION FROM OBJECT!!
  def __str__(self):
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


  

  
