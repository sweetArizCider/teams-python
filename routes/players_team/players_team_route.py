from fastapi import APIRouter, Path
from classes.player_team.PlayerTeamInterface import PlayerTeamRequest
from constants.response_constants import ServerStatus
from handlers.players_team.add.player_team_add_handler import player_team_add_handler
from handlers.players_team.retrieve.player_team_retrieve_handler import player_team_retrieve_handler
from handlers.players_team.update.player_team_update_handler import player_team_update_handler
from handlers.players_team.delete.player_team_delete_handler import player_team_delete_handler

SERVER_STATUS = ServerStatus()

router = APIRouter()

@router.get("/")
async def get_all_player_team_relationships():
    """Get all player-team relationships from MongoDB using PlayerTeam class"""
    return player_team_retrieve_handler.get_all_player_teams()

@router.get("/{relationship_id}")
async def get_player_team_by_id(relationship_id: str = Path(..., description="The ID of the relationship")):
    """Get a specific player-team relationship by ID using PlayerTeam class"""
    return player_team_retrieve_handler.get_player_team_by_id(relationship_id)

@router.get("/team/{team_id}/players")
async def get_players_by_team(team_id: str = Path(..., description="The ID of the team")):
    """Get all players for a specific team using Team and Player classes"""
    return player_team_retrieve_handler.get_players_by_team(team_id)

@router.get("/player/{player_id}/teams")
async def get_teams_by_player(player_id: str = Path(..., description="The ID of the player")):
    """Get all teams for a specific player using Team and Player classes"""
    return player_team_retrieve_handler.get_teams_by_player(player_id)

@router.post("/")
async def create_player_team_relationship(player_team: PlayerTeamRequest):
    """Create a new player-team relationship in MongoDB using PlayerTeam class"""
    return player_team_add_handler.add_player_team(player_team)

@router.put("/{relationship_id}")
async def update_player_team_relationship(
    player_team: PlayerTeamRequest,
    relationship_id: str = Path(..., description="The ID of the relationship")
):
    """Update a player-team relationship in MongoDB using PlayerTeam class"""
    return player_team_update_handler.update_player_team(relationship_id, player_team)

@router.delete("/{relationship_id}")
async def delete_player_team_relationship(relationship_id: str = Path(..., description="The ID of the relationship")):
    """Delete a player-team relationship from MongoDB using PlayerTeam class"""
    return player_team_delete_handler.delete_player_team(relationship_id)
