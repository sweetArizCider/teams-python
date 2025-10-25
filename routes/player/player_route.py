from fastapi import APIRouter, Path
from classes.player.PlayerInterface import PlayerRequest
from constants.response_constants import ServerStatus
from handlers.player.add.player_add_handler import player_add_handler
from handlers.player.retrieve.player_retrieve_handler import player_retrieve_handler
from handlers.player.update.player_update_handler import player_update_handler
from handlers.player.delete.player_delete_handler import player_delete_handler

SERVER_STATUS = ServerStatus()

router = APIRouter()

@router.get("/")
async def get_all_players():
    """Get all players from MongoDB using Player class"""
    return player_retrieve_handler.get_all_players()

@router.get("/{player_id}")
async def get_player_by_id(player_id: str = Path(..., description="The ID of the player")):
    """Get a specific player by ID using Player class"""
    return player_retrieve_handler.get_player_by_id(player_id)

@router.post("/")
async def create_player(player: PlayerRequest):
    """Create a new player in MongoDB using Player class"""
    return player_add_handler.add_player(player)

@router.put("/{player_id}")
async def update_player(player: PlayerRequest, player_id: str = Path(..., description="The ID of the player")):
    """Update a player in MongoDB using Player class"""
    return player_update_handler.update_player(player_id, player)

@router.delete("/{player_id}")
async def delete_player(player_id: str = Path(..., description="The ID of the player")):
    """Delete a player from MongoDB using Player class"""
    return player_delete_handler.delete_player(player_id)
