class Player:
  def __init__(self, name = '', age = 0, players = []):
    self.players = players
    self.name = name
    self.age = age
    self.index = 0
    

  def __str__(self):
    return f"Player: {self.name}, Age: {self.age}"
    
  def add_player(self, player):
    if len(self.name) > 0 or self.age > 0:
      return print("This is not an array of Players!")
    self.players.append({
      'name': player['name'], 
      'age': player['age'], 
      'index': self.index
    })
    self.index += 1
    return print(f"New player added: Name: {player['name']}")

  def remove_player(self, player_index):
    if not self.players:
      return print("There's no players to remove!")
    if player_index >= len(self.players) or player_index < 0:
      return print("Player index out of range!")
    if len(self.name) > 0 or self.age > 0:
      return print("This is not an array of Players!")
    self.players.remove(self.players[player_index])

  def update_player(self, new_name = '', new_age = 0, player_index = None):

    if player_index is None:
      if not self.players and (len(self.name) > 0 or self.age > 0):
        if new_name:
            self.name = new_name
        if new_age:
            self.age = new_age
        return print("Single player updated!")
      if self.players:
        return print("This is not a single player!")
      return print("Nothing to update!")

    if player_index is not None:
      if not self.players:
        return print("There's no players to update!")
      if player_index >= len(self.players) or player_index < 0:
        return print("Player index out of range!")
      if len(self.name) > 0:
        self.players[player_index]['name'] = self.name
      if self.age > 0:
        self.players[player_index]['age'] = self.age
      return print("Player updated!")

  def show_player_list(self):
    if not self.players:
      return print("This is not an Array of Players!")
    for player in self.players:
      print(f"Player index: {player['index']} -> {player['name']}, Age: {player['age']}")
  
  def show_player(self):
    if len(self.name) > 0 or self.age > 0:
      return print(f"Player: {self.name}, Age: {self.age}")
    return print("This is not a single Player!")

if __name__ == '__main__':

  # Creating a single player
  print("=================SINGLE PLAYER=================")
  single_player = Player('Carlos', 21)
  single_player.show_player()
  single_player.update_player(new_name='Pamela', new_age=19)
  single_player.show_player()

  print("=================PLAYERS ARRAY=================")

  # Creating an array of players
  players_array = Player()
  players_array.add_player({'name': 'Carlos', 'age': 21})
  players_array.add_player({'name': 'Pamela', 'age': 19})
  players_array.show_player_list()

  # TODO fix the update_player method for arrays
  players_array.update_player(new_name='Jose', new_age=22, player_index=0)
  players_array.show_player_list()

  
