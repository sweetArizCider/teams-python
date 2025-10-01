from team import Team
from player import Player
from object import Object

def json_to_object(json):
  team_data = json['Team']
  players_data = json['Players']

  team_object = Team(team_data['name'], team_data['sport'], team_data['city'])

  players_array_instance = Player()

  # Add each player from the players data
  for player_dict in players_data:
    temporal_player = Player(
      player_dict['name'],
      player_dict['age'],
      player_dict.get('number'),
      player_dict.get('nationality'),
      player_dict.get('position')
    )
    players_array_instance.add(temporal_player)

  return PlayerTeam(team_object, players_array_instance)

class PlayerTeam(Object):
  def __init__(self, team: Team = None, players: Player = None):
    is_array = (team is None and players is None)
    super().__init__(is_array=is_array)

    if not self.is_array:
      if team is None or players is None:
        raise ValueError("Both 'team' and 'players' are required for a PlayerTeam.")
      self.team = team
      self.players = players

  def __str__(self):
    if self.is_array:
      return super().__str__()
    team_str = str(self.team)
    return f"Team_Object: {team_str},\nPlayers count: {self.players}"

  def dictionary_team(self):
    if not self.is_array:
      return {
        "Team": self.team.dictionary(),
        "Players": self.players.dictionary()
      }
    return [object.dictionary_team() for object in self.object_array]


if __name__ == '__main__':
  cruz_azul = Team('Cruz Azul', 'Soccer', 'Mexico City')
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

  player_team = PlayerTeam(cruz_azul, players_array)

  players_team_array = PlayerTeam()
  players_team_array.add(player_team)
  players_team_array.list()

  print("=================PLAYERS TEAM ARRAY=================")
  cruz_azul_json = player_team.dictionary_team()
  print(cruz_azul_json)
  cruz_azul_object = json_to_object(cruz_azul_json)
  print(cruz_azul_object)