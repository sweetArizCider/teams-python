class Player:
  def __init__(
      self, 
      name = None, 
      age = None,  
      number = None, #optional
      nationality = None, #optional
      position = None #optional
    ):
    # Name and Age are required to create an object!!
    if not (name == None or age == None):
      self.name = name
      self.age = age
      self.number = number
      self.nationality = nationality
      self.position = position
      self.is_array = False
      return
    
    self.is_array = True
    self.players = []
    self.index = 0
    
  def __str__(self):
    return f"Player: {self.name} \nAge: {self.age} \nNumber: {self.number} \nNationality: {self.nationality} \nPosition: {self.position}"
  
  def add_player(self, player):
    if not self.is_array:
      return print("This is not an Array of players!, player not added")
    player.index = len(self.players)
    self.players.append(player)
    return print("Player added!")

  def list_players(self):
    if not self.is_array:
      return print("This is not an Array of players!")
    for player in self.players:
      print(f"\n{player}")
    return

  def update_player(self, index, new_name = None, new_age = None, new_number = None, new_nationality = None, new_position = None):
    if index == None:
      return print("Index is required!!")
    if not self.is_array:
      return print("This is not an array of players!!")
    player = self.players[index]

    if new_name:
      player.name = new_name
    if new_age:
      player.age = new_age
    if new_number:
      player.number = new_number
    if new_nationality:
      player.nationality = new_nationality
    if new_position:
      player.position = new_position
    return print("Player updated!")

  def remove_player(self, index):
    if index == None:
      return print("Index is required!!")
    if not self.is_array:
      return print("This is not an array of players!!")
    self.players.pop(index)
    return print("Player removed!")

if __name__ == '__main__':

  # Creating a single player
  print("=================SINGLE PLAYER=================")
  single_player = Player('Carlos', 21)
  single_player2 = Player('Pamela', 19, 16, 'Mexico', 'Goalkeeper')
  single_player3 = Player('Jose', 32, 2, 'Mexico', 'Defensor')
  print(single_player2)

  print("=================PLAYERS ARRAY=================")
  players_array = Player()
  players_array.add_player(single_player2)
  players_array.add_player(single_player)
  players_array.add_player(single_player3)

  players_array.update_player(index=0, new_name='Carlos A.', new_age=22, new_number=10, new_nationality='Mexico', new_position='Midfielder')
  players_array.update_player(index=1, new_age=20)
  players_array.remove_player(index=2)
  players_array.list_players()

  

  
