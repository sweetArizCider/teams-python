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
    if not (name == None or name == None):
      self.name = name
      self.age = age
      self.number = number if number is not None else None
      self.nationality = nationality if nationality is not None else None
      self.position = position if position is not None else None
    else:
      super().__init__()

  # TODO COMPLETE THE EXTENTION FROM OBJECT!!
    
if __name__ == '__main__':

  # Creating a single player
  print("=================SINGLE PLAYER=================")
  single_player = Player('Carlos', 21)
  single_player2 = Player('Pamela', 19, 16, 'Mexico', 'Goalkeeper')
  single_player3 = Player('Jose', 32, 2, 'Mexico', 'Defensor')
  single_player4 = Player('Luis', 45, 76)
  print(single_player)


  print("=================PLAYERS ARRAY=================")
  players_array = Player()
  players_array.add_player(single_player)
  players_array.add_player(single_player2)
  players_array.add_player(single_player3)
  players_array.add_player(single_player4)

  players_array.update_player(index=0, new_name='Carlos A.', new_age=22, new_number=10, new_nationality='Mexico', new_position='Midfielder')
  players_array.update_player(index=1, new_age=20)
  players_array.remove_player(index=2)
  players_array.list_players()

  

  
