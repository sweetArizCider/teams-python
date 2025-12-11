from bson import ObjectId
from typing import Dict, Any
from classes.database.database import mongodb_service
from classes.database.json_storage import json_storage
from classes.database.sync_service import sync_service
from classes.team.team import Team
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class TeamDeleteHandler:
    def __init__(self):
        self.collection = None
        self._update_collection()

    def _update_collection(self):
        """Update collection reference if not offline"""
        if not mongodb_service.is_offline:
            self.collection = mongodb_service.get_teams_collection()

    def delete_team(self, team_id: str) -> Dict[str, Any]:
        """Delete a team using validation from Team class"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collection()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()

            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info(f"Using local JSON storage to delete team {team_id}")

                existing_team = json_storage.get_team_by_id(team_id)
                if not existing_team:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Team not found"
                    }

                team_name = existing_team.get("name")
                success = json_storage.delete_team(team_id)

                if not success:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Team not found or already deleted"
                    }

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": f"Team '{team_name}' deleted successfully (offline mode)"
                }

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
            # Fallback to JSON storage
            try:
                logger.info("Falling back to JSON storage due to error")
                existing_team = json_storage.get_team_by_id(team_id)
                if not existing_team:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Team not found"
                    }

                team_name = existing_team.get("name")
                success = json_storage.delete_team(team_id)

                if not success:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Team not found or already deleted"
                    }

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": f"Team '{team_name}' deleted successfully (offline mode)"
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

# Create a global instance
team_delete_handler = TeamDeleteHandler()
