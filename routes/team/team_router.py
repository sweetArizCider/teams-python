from fastapi import APIRouter, Path
from classes.team.TeamInterface import TeamRequest
from constants.response_constants import ServerStatus
from handlers.team.add.team_add_handler import team_add_handler
from handlers.team.retrieve.team_retrieve_handler import team_retrieve_handler
from handlers.team.update.team_update_handler import team_update_handler
from handlers.team.delete.team_delete_handler import team_delete_handler

SERVER_STATUS = ServerStatus()

router = APIRouter()

@router.get("/")
async def get_all_teams():
    """Get all teams from MongoDB using Team class"""
    return team_retrieve_handler.get_all_teams()

@router.get("/{team_id}")
async def get_team_by_id(team_id: str = Path(..., description="The ID of the team")):
    """Get a specific team by ID using Team class"""
    return team_retrieve_handler.get_team_by_id(team_id)

@router.post("/")
async def create_team(team: TeamRequest):
    """Create a new team in MongoDB using Team class"""
    return team_add_handler.add_team(team)

@router.put("/{team_id}")
async def update_team(team: TeamRequest, team_id: str = Path(..., description="The ID of the team")):
    """Update a team in MongoDB using Team class"""
    return team_update_handler.update_team(team_id, team)

@router.delete("/{team_id}")
async def delete_team(team_id: str = Path(..., description="The ID of the team")):
    """Delete a team from MongoDB using Team class"""
    return team_delete_handler.delete_team(team_id)
