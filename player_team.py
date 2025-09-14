from team import Team
from player import Player
from object import Object

class PlayerTeam(Object):
  def __init__(self, team: Team = None, players: list[Player] = None):
    if not (team is None or players is None):
      self.team = team
      self.players = players
    else:
      super().__init__()
  
  def __str__(self):
    return f"Team_Object: {self.team},\nPlayers count: {len(self.players)}, \nPlayers_Object: {', '.join([player.name for player in self.players])}"

if __name__ == '__main__':
  cruz_azul = Team('Cruz Azul', 'Soccer', 'Mexico City')
  carlos = Player('Carlos Arizpe', 21)
  sofia = Player("Sofía Delgado", 19)

  pumas = Team('Pumas', 'Soccer', 'CDMX')
  ana = Player('Ana Martinez', 29, 10, 'Spain', 'Midfielder')
  luis = Player('Luis Garcia', 25, 7, 'Mexico', 'Forward')

  player_team = PlayerTeam(cruz_azul, [carlos, sofia])
  player_team2 = PlayerTeam(pumas, [ana, luis])

  players_team_array = PlayerTeam()
  players_team_array.add(player_team)
  players_team_array.add(player_team2)
  players_team_array.update(index=1, object_element=PlayerTeam(pumas, [ana, luis, sofia]))
  players_team_array.list()