from bson import ObjectId
from typing import Dict, Any
from classes.database.database import mongodb_service
from classes.player_team.player_team import PlayerTeam
from classes.team.team import Team
from classes.player.Player import Player
from classes.player_team.PlayerTeamInterface import PlayerTeamRequest
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class PlayerTeamUpdateHandler:
    def __init__(self):
        self.collection = mongodb_service.get_players_team_collection()
        self.players_collection = mongodb_service.get_players_collection()
        self.teams_collection = mongodb_service.get_teams_collection()

    def update_player_team(self, relationship_id: str, player_team_request: PlayerTeamRequest) -> Dict[str, Any]:
        """Update a player-team relationship using the PlayerTeam class"""
        try:
            # Validate ObjectId format for relationship ID
            if not ObjectId.is_valid(relationship_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid relationship ID format"
                }

            # Validate that player_id and team_id are valid ObjectIds
            if not ObjectId.is_valid(player_team_request.player_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid player ID format"
                }

            if not ObjectId.is_valid(player_team_request.team_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid team ID format"
                }

            # Verify that the player and team exist
            player_doc = self.players_collection.find_one({"_id": ObjectId(player_team_request.player_id)})
            if not player_doc:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Player not found"
                }

            team_doc = self.teams_collection.find_one({"_id": ObjectId(player_team_request.team_id)})
            if not team_doc:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Team not found"
                }

            # Create Player and Team instances for validation using your existing classes
            player = Player(
                name=player_doc.get("name"),
                age=player_doc.get("age"),
                number=player_doc.get("number"),
                nationality=player_doc.get("nationality"),
                position=player_doc.get("position")
            )

            team = Team(
                name=team_doc.get("name"),
                sport=team_doc.get("sport"),
                city=team_doc.get("city")
            )

            # Create a Player array instance and add the single player using your class methods
            players_array = Player()
            players_array.add(player)

            # Create PlayerTeam instance for validation using your existing class
            player_team = PlayerTeam(team=team, players=players_array)

            # Log the update operation using your class's __str__ method
            logger.info(f"Updating player-team relationship: {player_team}")

            # Prepare updated data for MongoDB (relationship data, not full objects)
            update_data = {
                "player_id": ObjectId(player_team_request.player_id),
                "team_id": ObjectId(player_team_request.team_id),
                "position": player_team_request.position,
                "jersey_number": player_team_request.jersey_number,
                "start_date": player_team_request.start_date,
                "end_date": player_team_request.end_date,
                "is_active": player_team_request.is_active
            }

            # Update in MongoDB
            result = self.collection.update_one(
                {"_id": ObjectId(relationship_id)},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Player-team relationship not found"
                }

            # Get the updated relationship from MongoDB
            updated_relationship = self.collection.find_one({"_id": ObjectId(relationship_id)})
            updated_relationship["_id"] = str(updated_relationship["_id"])
            updated_relationship["player_id"] = str(updated_relationship["player_id"])
            updated_relationship["team_id"] = str(updated_relationship["team_id"])

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": "Player-team relationship updated successfully",
                "data": updated_relationship
            }

        except ValueError as ve:
            logger.error(f"Validation error updating player-team relationship {relationship_id}: {str(ve)}")
            return {
                "status": SERVER_STATUS.BAD_REQUEST.CODE,
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            logger.error(f"Error updating player-team relationship {relationship_id}: {str(e)}")
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

# Create a global instance
player_team_update_handler = PlayerTeamUpdateHandler()
