from bson import ObjectId
from typing import Dict, Any
from classes.database.database import mongodb_service
from classes.team.team import Team
from classes.team.TeamInterface import TeamRequest
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class TeamUpdateHandler:
    def __init__(self):
        self.collection = mongodb_service.get_teams_collection()

    def update_team(self, team_id: str, team_request: TeamRequest) -> Dict[str, Any]:
        """Update a team using the Team class"""
        try:
            # Validate ObjectId format
            if not ObjectId.is_valid(team_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid team ID format"
                }

            # Create Team instance with updated data
            updated_team = Team(
                name=team_request.name,
                sport=team_request.sport,
                city=team_request.city
            )

            # Use your existing dictionary() method from Object class
            update_data = updated_team.dictionary()

            # Update in MongoDB
            result = self.collection.update_one(
                {"_id": ObjectId(team_id)},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Team not found"
                }

            # Get the updated team from MongoDB
            updated_team_doc = self.collection.find_one({"_id": ObjectId(team_id)})
            updated_team_doc["_id"] = str(updated_team_doc["_id"])

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": "Team updated successfully",
                "data": updated_team_doc
            }

        except ValueError as ve:
            logger.error(f"Validation error updating team {team_id}: {str(ve)}")
            return {
                "status": SERVER_STATUS.BAD_REQUEST.CODE,
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            logger.error(f"Error updating team {team_id}: {str(e)}")
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

# Create a global instance
team_update_handler = TeamUpdateHandler()
