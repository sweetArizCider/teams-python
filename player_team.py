from team import Team
from player import Player

class PlayerTeam:
  def __init__(self, team: Team, players: list[Player]):
    self.team = team.name
    self.players = players

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