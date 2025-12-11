from bson import ObjectId
from typing import Dict, Any
from classes.database.database import mongodb_service
from classes.database.json_storage import json_storage
from classes.database.sync_service import sync_service
from classes.team.team import Team
from classes.team.TeamInterface import TeamRequest
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class TeamUpdateHandler:
    def __init__(self):
        self.collection = None
        self._update_collection()

    def _update_collection(self):
        """Update collection reference if not offline"""
        if not mongodb_service.is_offline:
            self.collection = mongodb_service.get_teams_collection()

    def update_team(self, team_id: str, team_request: TeamRequest) -> Dict[str, Any]:
        """Update a team using the Team class"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collection()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()

            # Create Team instance with updated data
            updated_team = Team(
                name=team_request.name,
                sport=team_request.sport,
                city=team_request.city
            )

            # Use your existing dictionary() method from Object class
            update_data = updated_team.dictionary()

            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info(f"Using local JSON storage to update team {team_id}")
                success = json_storage.update_team(team_id, update_data)

                if not success:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Team not found"
                    }

                updated_team_doc = json_storage.get_team_by_id(team_id)
                updated_team_doc["_id"] = str(updated_team_doc["_id"])

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": "Team updated successfully (offline mode - will sync when online)",
                    "data": updated_team_doc
                }

            # Validate ObjectId format
            if not ObjectId.is_valid(team_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid team ID format"
                }

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
            # Fallback to JSON storage
            try:
                logger.info("Falling back to JSON storage due to error")
                updated_team = Team(
                    name=team_request.name,
                    sport=team_request.sport,
                    city=team_request.city
                )
                update_data = updated_team.dictionary()
                success = json_storage.update_team(team_id, update_data)

                if not success:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Team not found"
                    }

                updated_team_doc = json_storage.get_team_by_id(team_id)
                updated_team_doc["_id"] = str(updated_team_doc["_id"])

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": "Team updated successfully (offline mode - will sync when online)",
                    "data": updated_team_doc
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

# Create a global instance
team_update_handler = TeamUpdateHandler()
