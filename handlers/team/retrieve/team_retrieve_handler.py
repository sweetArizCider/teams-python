from bson import ObjectId
from typing import Dict, Any, List
from classes.database.database import mongodb_service
from classes.database.json_storage import json_storage
from classes.database.sync_service import sync_service
from classes.team.team import Team
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class TeamRetrieveHandler:
    def __init__(self):
        self.collection = None
        self._update_collection()

    def _update_collection(self):
        """Update collection reference if not offline"""
        if not mongodb_service.is_offline:
            self.collection = mongodb_service.get_teams_collection()

    def get_all_teams(self) -> Dict[str, Any]:
        """Get all teams using the Team class array functionality"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collection()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()

            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info("Using local JSON storage for teams")
                teams_data = json_storage.get_all_teams()

                teams_array = Team()

                for team_doc in teams_data:
                    team = Team(
                        name=team_doc.get("name"),
                        sport=team_doc.get("sport"),
                        city=team_doc.get("city")
                    )
                    team._id = team_doc["_id"]
                    teams_array.add(team)

                teams_dict_array = teams_array.dictionary()
                for i, team_dict in enumerate(teams_dict_array):
                    if hasattr(teams_array.object_array[i], '_id'):
                        team_dict["_id"] = teams_array.object_array[i]._id

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode)",
                    "data": teams_dict_array
                }

            # Get all documents from MongoDB
            teams_data = list(self.collection.find())

            # Create a Team array instance
            teams_array = Team()  # This creates an array instance

            # Convert each MongoDB document to Team object and add to array
            for team_doc in teams_data:
                # Convert ObjectId to string for the document
                team_doc["_id"] = str(team_doc["_id"])

                # Create Team instance from MongoDB data
                team = Team(
                    name=team_doc.get("name"),
                    sport=team_doc.get("sport"),
                    city=team_doc.get("city")
                )

                # Add the _id to the team object for response
                team._id = team_doc["_id"]

                teams_array.add(team)

            # Use your existing dictionary() method from Object class
            teams_dict_array = teams_array.dictionary()

            # Add _id to each team dictionary
            for i, team_dict in enumerate(teams_dict_array):
                if hasattr(teams_array.object_array[i], '_id'):
                    team_dict["_id"] = teams_array.object_array[i]._id

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": SERVER_STATUS.SUCCESS.MESSAGE,
                "data": teams_dict_array
            }

        except Exception as e:
            logger.error(f"Error retrieving teams: {str(e)}")
            # Fallback to JSON storage
            try:
                logger.info("Falling back to JSON storage due to error")
                teams_data = json_storage.get_all_teams()
                teams_array = Team()

                for team_doc in teams_data:
                    team = Team(
                        name=team_doc.get("name"),
                        sport=team_doc.get("sport"),
                        city=team_doc.get("city")
                    )
                    team._id = team_doc["_id"]
                    teams_array.add(team)

                teams_dict_array = teams_array.dictionary()
                for i, team_dict in enumerate(teams_dict_array):
                    if hasattr(teams_array.object_array[i], '_id'):
                        team_dict["_id"] = teams_array.object_array[i]._id

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode - fallback)",
                    "data": teams_dict_array
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

    def get_team_by_id(self, team_id: str) -> Dict[str, Any]:
        """Get a specific team by ID using the Team class"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collection()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()

            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info(f"Using local JSON storage for team {team_id}")
                team_doc = json_storage.get_team_by_id(team_id)

                if not team_doc:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Team not found"
                    }

                team = Team(
                    name=team_doc.get("name"),
                    sport=team_doc.get("sport"),
                    city=team_doc.get("city")
                )

                team_dict = team.dictionary()
                team_dict["_id"] = team_doc["_id"]

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode)",
                    "data": team_dict
                }

            # Validate ObjectId format
            if not ObjectId.is_valid(team_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid team ID format"
                }

            # Find team in MongoDB
            team_doc = self.collection.find_one({"_id": ObjectId(team_id)})

            if not team_doc:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Team not found"
                }

            # Convert ObjectId to string
            team_doc["_id"] = str(team_doc["_id"])

            # Create Team instance from MongoDB data
            team = Team(
                name=team_doc.get("name"),
                sport=team_doc.get("sport"),
                city=team_doc.get("city")
            )

            # Use your existing dictionary() method from Object class
            team_dict = team.dictionary()
            team_dict["_id"] = team_doc["_id"]

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": SERVER_STATUS.SUCCESS.MESSAGE,
                "data": team_dict
            }

        except ValueError as ve:
            logger.error(f"Validation error retrieving team {team_id}: {str(ve)}")
            return {
                "status": SERVER_STATUS.BAD_REQUEST.CODE,
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            logger.error(f"Error retrieving team {team_id}: {str(e)}")
            # Fallback to JSON storage
            try:
                logger.info("Falling back to JSON storage due to error")
                team_doc = json_storage.get_team_by_id(team_id)

                if not team_doc:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Team not found"
                    }

                team = Team(
                    name=team_doc.get("name"),
                    sport=team_doc.get("sport"),
                    city=team_doc.get("city")
                )

                team_dict = team.dictionary()
                team_dict["_id"] = team_doc["_id"]

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode - fallback)",
                    "data": team_dict
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

# Create a global instance
team_retrieve_handler = TeamRetrieveHandler()
