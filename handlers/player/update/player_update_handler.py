from classes.player.PlayerInterface import PlayerRequest, PlayerArrayRequest
from classes.player.Player import Player


def update_player_in_array(players_array_data: PlayerArrayRequest, index: int, updated_player_data: PlayerRequest):
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

  updated_player = Player(
    name=updated_player_data.name,
    age=updated_player_data.age,
    number=updated_player_data.number,
    nationality=updated_player_data.nationality,
    position=updated_player_data.position
  )

  players_array_instance.update(index, updated_player)

  return players_array_instance