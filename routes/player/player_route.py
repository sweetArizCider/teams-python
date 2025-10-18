from fastapi import APIRouter
from handlers.player.create.player_create_handler import create_single_player, create_players_array
from handlers.player.add.player_add_handler import add_player_to_array
from classes.player.PlayerInterface import PlayerRequest, PlayerArrayRequest
from constants.response_constants import ServerStatus
from handlers.player.delete.player_delete_handler import remove_player_from_array
from handlers.player.update.player_update_handler import update_player_in_array

SERVER_STATUS = ServerStatus()

router = APIRouter()

@router.post("/")
async def create_single_player_endpoint(player: PlayerRequest):
  try:
    new_player = create_single_player(
        name=player.name,
        age=player.age,
        number=player.number,
        nationality=player.nationality,
        position=player.position
    )
    return {
      "status": SERVER_STATUS.CREATED.CODE,
      "message": SERVER_STATUS.CREATED.MESSAGE,
      "data": {
        "name": new_player.name,
        "age": new_player.age,
        "number": new_player.number,
        "nationality": new_player.nationality,
        "position": new_player.position,
      }
    }
  except Exception as e:
    return {
      "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
      "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
    }

@router.post("/array")
def create_players_array_endpoint():
  players_array_instance = create_players_array()
  return {
    "status": SERVER_STATUS.CREATED.CODE,
    "message": SERVER_STATUS.CREATED.MESSAGE,
    "data": {
        "players_count": len(players_array_instance.object_array),
        "is_array": players_array_instance.is_array,
        "message": "Empty players array created successfully"
    }
  }

@router.post("/add")
def add_player_to_array_endpoint(players_array: PlayerArrayRequest, player: PlayerRequest):
  try:
    updated_players_array = add_player_to_array(players_array, player)
    return {
      "status": SERVER_STATUS.SUCCESS.CODE,
      "message": SERVER_STATUS.SUCCESS.MESSAGE,
      "data": {
          "players_count": len(updated_players_array.object_array),
          "is_array": updated_players_array.is_array,
          "message": "Player added successfully"
      }
    }
  except Exception as e:
    return {
      "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
      "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
    }

@router.delete("/")
def delete_players_array_endpoint(players_array: PlayerArrayRequest, index: int):
  try:
    updated_players_array = remove_player_from_array(players_array, index)
    return {
      "status": SERVER_STATUS.SUCCESS.CODE,
      "message": SERVER_STATUS.SUCCESS.MESSAGE,
      "data": {
          "players_count": len(updated_players_array.object_array),
          "is_array": updated_players_array.is_array,
          "message": "Player removed successfully"
      }
    }
  except IndexError as ie:
    return {
      "status": SERVER_STATUS.BAD_REQUEST.CODE,
      "message": f"{SERVER_STATUS.BAD_REQUEST.MESSAGE}: {str(ie)}"
    }
  except Exception as e:
    return {
      "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
      "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
    }

@router.put("/update")
def update_player_in_array_endpoint(players_array: PlayerArrayRequest, updated_player: PlayerRequest, index: int):
  try:
    updated_players_array = update_player_in_array(players_array, index, updated_player)
    return {
      "status": SERVER_STATUS.SUCCESS.CODE,
      "message": SERVER_STATUS.SUCCESS.MESSAGE,
      "data": {
          "players_count": len(updated_players_array.object_array),
          "is_array": updated_players_array.is_array,
          "message": "Player updated successfully"
      }
    }
  except IndexError as ie:
    return {
      "status": SERVER_STATUS.BAD_REQUEST.CODE,
      "message": f"{SERVER_STATUS.BAD_REQUEST.MESSAGE}: {str(ie)}"
    }
  except Exception as e:
    return {
      "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
      "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
    }
