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
  single_player = Player('Lionel Messi', 36, 10, 'Argentina', 'Forward')
  single_player.to_json_file('single_player.json')

  players = Player()
  players.add(Player('Cristiano Ronaldo', 39, 7, 'Portugal', 'Forward'))
  players.add(Player('Neymar Jr', 32, 10, 'Brazil', 'Forward'))
  players.list()
  players.to_json_file('players.json')

  player_instance = Player()
  loaded_players = player_instance.json_to_object('players.json')
  print("\nLoaded players:")
  print(loaded_players)

  loaded_players.list()
  

  
