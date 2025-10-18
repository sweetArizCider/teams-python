from classes.player.PlayerInterface import PlayerRequest, PlayerArrayRequest
from classes.player.Player import Player

def add_player_to_array(players_array_data: PlayerArrayRequest, player_data: PlayerRequest):
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

    new_player = Player(
        name=player_data.name,
        age=player_data.age,
        number=player_data.number,
        nationality=player_data.nationality,
        position=player_data.position
    )

    players_array_instance.add(new_player)

    return players_array_instance