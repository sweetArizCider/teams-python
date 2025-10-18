from classes.player.PlayerInterface import PlayerRequest, PlayerArrayRequest
from classes.player.Player import Player


def remove_player_from_array(players_array_data: PlayerArrayRequest, index: int):
  players_array_instance = Player()

  if players_array_data.object_array:
    for player_req in players_array_data.object_array:
      existing_player = Player(
        name=player_req.name,
        age=player_req.age,
        number=player_req.number,
        nationality=player_req.nationality,
        position=player_req.position
      )
      players_array_instance.add(existing_player)

  players_array_instance.remove(index)

  return players_array_instance
