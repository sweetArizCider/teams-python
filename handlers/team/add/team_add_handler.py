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

class TeamAddHandler:
    def __init__(self):
        self.collection = None
        self._update_collection()

    def _update_collection(self):
        """Update collection reference if not offline"""
        if not mongodb_service.is_offline:
            self.collection = mongodb_service.get_teams_collection()

    def add_team(self, team_request: TeamRequest) -> Dict[str, Any]:
        """Add a new team using the Team class"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collection()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()

            # Create Team instance using the existing Team class
            team = Team(
                name=team_request.name,
                sport=team_request.sport,
                city=team_request.city
            )

            # Use your existing dictionary() method from Object class
            team_data = team.dictionary()

            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info("Using local JSON storage to add team")
                created_team = json_storage.add_team(team_data)

                return {
                    "status": SERVER_STATUS.CREATED.CODE,
                    "message": SERVER_STATUS.CREATED.MESSAGE + " (offline mode - will sync when online)",
                    "data": created_team
                }

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
            # On error, try JSON storage as fallback
            try:
                logger.info("Falling back to JSON storage due to error")
                team = Team(
                    name=team_request.name,
                    sport=team_request.sport,
                    city=team_request.city
                )
                team_data = team.dictionary()
                created_team = json_storage.add_team(team_data)

                return {
                    "status": SERVER_STATUS.CREATED.CODE,
                    "message": SERVER_STATUS.CREATED.MESSAGE + " (offline mode - will sync when online)",
                    "data": created_team
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

# Create a global instance
team_add_handler = TeamAddHandler()
