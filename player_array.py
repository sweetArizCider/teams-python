class Player:
  def __init__(self, name = '', age = 0, players = []):
    self.players = players
    self.name = name
    self.age = age
    

  def __str__(self):
    return f"This is a single Player! -> {self.name}, {self.age}"
    
  def add_player(self, player):
    self.players.append(player)
    return print(f"New player added: {player}")
  
  def remove_player(self, player_index):
    if not self.players:
      return print("This is not an Array of Players!")
    self.players.remove[player_index]
  
  def show_player_list(self):
    return print(f"{self.players}")

if __name__ == '__main__':
  carlos = Player('Carlos', 23)
  jose = Player('Jose', 21)
  array = Player()
  
  array.add_player({'name': 'Carlos', 'age': 21})
  array.add_player({'name': 'Pamepla', 'age': 19})
  array.show_player_list()
  print(carlos)
