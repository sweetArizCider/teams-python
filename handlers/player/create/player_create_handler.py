from classes.player.Player import Player

def create_single_player(
    name: str,
    age: int,
    number: int = None,
    nationality: str = None,
    position: str = None
):
  number = int(number) if number is not None else None
  nationality = str(nationality) if nationality is not None else None
  position = str(position) if position is not None else None

  new_player = Player(
    name,
    age,
    number = int(number) if number is not None else None,
    nationality=str(nationality) if nationality is not None else None,
    position=str(position) if position is not None else None
  )

  return new_player

def create_players_array():
  players_array_instance = Player()
  return players_array_instance