from classes.team.team import Team
from classes.player.Player import Player
from classes.object.object import Object
import json

def json_to_object(json):
  team_data = json['Team']
  players_data = json['Players']

  team_object = Team(team_data['name'], team_data['sport'], team_data['city'])

  players_array_instance = Player()

  for player_json in players_data:
    temporal_player = Player(
      player_json['name'],
      player_json['age'],
      player_json.get('number'),
      player_json.get('nationality'),
      player_json.get('position')
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

  def to_json_file(self, filename):
    data = self.dictionary_team()

    with open(filename, 'w', encoding='utf-8') as json_file:
      json.dump(data, json_file, indent=2, ensure_ascii=False)
    print(f"PlayerTeam saved to {filename}")

  def json_to_object(self, json_file):
    with open(json_file, 'r', encoding='utf-8') as json_file_data:
      data = json.load(json_file_data)

    if isinstance(data, list):
      object_array_instance = self.__class__()
      for item in data:
        temporal_object = json_to_object(item)
        object_array_instance.add(temporal_object)
      return object_array_instance
    return json_to_object(data)

if __name__ == '__main__':
  players_array_instance = PlayerTeam()
  loaded_team_object = players_array_instance.json_to_object('single_player_team.json')
  loaded_team_object.to_json_file('test.json')
  print(loaded_team_object)
