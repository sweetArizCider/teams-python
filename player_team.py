from team import Team
from player import Player

class PlayerTeam:
  def __init__(self, team: Team, players: list[Player]):
    self.team = team.name
    self.players = players
  
  def __str__(self):
    return f"Team: {self.team}, Players count: {len(self.players)}, Players: {', '.join([player.name for player in self.players])}"

  def add_player(self, player):
    if not player:
      return
    self.players.append(player)

  def remove_player(self, player):
    if not player:
      return
    self.players.remove(player)

  def list_players(self):
    print(f"Players in {self.team}")
    for player in self.players:
      print(player.name)

if __name__ == '__main__':
  cruz_azul = Team('Cruz Azul', 'Soccer')
  carlos = Player('Carlos Arizpe', 21)
  sofia = Player("Sofía Delgado", 19)
  marco = Player("Marco Ruiz", 22)
  ana = Player("Ana Fernández", 20)
  liam = Player("Liam Torres", 23)
  valeria = Player("Valeria Gómez", 18)
  diego = Player("Diego Navarro", 24)
  lucia = Player("Lucía Herrera", 21)
  mateo = Player("Mateo Castillo", 20)
  elena = Player("Elena Rivas", 22)
  bruno = Player("Bruno Morales", 19)

  players = [
      carlos,
      sofia,
      marco,
      ana,
      liam,
      valeria,
      diego,
      lucia,
      mateo,
      elena,
      bruno,
  ]

  players_team = PlayerTeam(cruz_azul, players)
  print(players_team)