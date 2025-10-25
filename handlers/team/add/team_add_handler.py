from bson import ObjectId
from typing import Dict, Any
from classes.database.database import mongodb_service
from classes.team.team import Team
from classes.team.TeamInterface import TeamRequest
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class TeamAddHandler:
    def __init__(self):
        self.collection = mongodb_service.get_teams_collection()

    def add_team(self, team_request: TeamRequest) -> Dict[str, Any]:
        """Add a new team using the Team class"""
        try:
            # Create Team instance using the existing Team class
            team = Team(
                name=team_request.name,
                sport=team_request.sport,
                city=team_request.city
            )

            # Use your existing dictionary() method from Object class
            team_data = team.dictionary()

            # Insert into MongoDB
            result = self.collection.insert_one(team_data)

            # Get the created team from MongoDB
            created_team = self.collection.find_one({"_id": result.inserted_id})
            created_team["_id"] = str(created_team["_id"])  # Convert ObjectId to string

            return {
                "status": SERVER_STATUS.CREATED.CODE,
                "message": SERVER_STATUS.CREATED.MESSAGE,
                "data": created_team
            }

        except ValueError as ve:
            logger.error(f"Validation error creating team: {str(ve)}")
            return {
                "status": SERVER_STATUS.BAD_REQUEST.CODE,
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            logger.error(f"Error creating team: {str(e)}")
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

# Create a global instance
team_add_handler = TeamAddHandler()
