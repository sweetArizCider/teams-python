from bson import ObjectId
from typing import Dict, Any, List
from classes.database.database import mongodb_service
from classes.team.team import Team
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class TeamRetrieveHandler:
    def __init__(self):
        self.collection = mongodb_service.get_teams_collection()

    def get_all_teams(self) -> Dict[str, Any]:
        """Get all teams using the Team class array functionality"""
        try:
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
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

    def get_team_by_id(self, team_id: str) -> Dict[str, Any]:
        """Get a specific team by ID using the Team class"""
        try:
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
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

# Create a global instance
team_retrieve_handler = TeamRetrieveHandler()
