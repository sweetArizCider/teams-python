from bson import ObjectId
from typing import Dict, Any
from classes.database.database import mongodb_service
from classes.team.team import Team
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class TeamDeleteHandler:
    def __init__(self):
        self.collection = mongodb_service.get_teams_collection()

    def delete_team(self, team_id: str) -> Dict[str, Any]:
        """Delete a team using validation from Team class"""
        try:
            # Validate ObjectId format
            if not ObjectId.is_valid(team_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid team ID format"
                }

            # Check if team exists before deletion (optional but good practice)
            existing_team = self.collection.find_one({"_id": ObjectId(team_id)})
            if not existing_team:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Team not found"
                }

            # Create Team instance to log what's being deleted
            team_to_delete = Team(
                name=existing_team.get("name"),
                sport=existing_team.get("sport"),
                city=existing_team.get("city")
            )

            # Log the deletion for audit purposes
            logger.info(f"Deleting team: {team_to_delete}")

            # Delete from MongoDB
            result = self.collection.delete_one({"_id": ObjectId(team_id)})

            if result.deleted_count == 0:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Team not found or already deleted"
                }

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": f"Team '{team_to_delete.name}' deleted successfully"
            }

        except ValueError as ve:
            logger.error(f"Validation error deleting team {team_id}: {str(ve)}")
            return {
                "status": SERVER_STATUS.BAD_REQUEST.CODE,
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            logger.error(f"Error deleting team {team_id}: {str(e)}")
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

# Create a global instance
team_delete_handler = TeamDeleteHandler()
