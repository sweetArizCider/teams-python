from bson import ObjectId
from typing import Dict, Any
from classes.database.database import mongodb_service
from classes.player_team.player_team import PlayerTeam
from classes.team.team import Team
from classes.player.Player import Player
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class PlayerTeamDeleteHandler:
    def __init__(self):
        self.collection = mongodb_service.get_players_team_collection()
        self.players_collection = mongodb_service.get_players_collection()
        self.teams_collection = mongodb_service.get_teams_collection()

    def delete_player_team(self, relationship_id: str) -> Dict[str, Any]:
        """Delete a player-team relationship using validation from PlayerTeam class"""
        try:
            # Validate ObjectId format
            if not ObjectId.is_valid(relationship_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid relationship ID format"
                }

            # Check if relationship exists before deletion
            existing_relationship = self.collection.find_one({"_id": ObjectId(relationship_id)})
            if not existing_relationship:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Player-team relationship not found"
                }

            # Get player and team data for logging using your existing classes
            player_doc = self.players_collection.find_one({"_id": existing_relationship["player_id"]})
            team_doc = self.teams_collection.find_one({"_id": existing_relationship["team_id"]})

            if player_doc and team_doc:
                # Create Player and Team instances using your existing classes
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

                # Create PlayerTeam instance for logging using your existing class
                player_team_to_delete = PlayerTeam(team=team, players=players_array)

                # Log the deletion for audit purposes using your class's __str__ method
                logger.info(f"Deleting player-team relationship: {player_team_to_delete}")

            # Delete from MongoDB
            result = self.collection.delete_one({"_id": ObjectId(relationship_id)})

            if result.deleted_count == 0:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Player-team relationship not found or already deleted"
                }

            if player_doc and team_doc:
                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": f"Player-team relationship between '{player.name}' and '{team.name}' deleted successfully"
                }
            else:
                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": "Player-team relationship deleted successfully"
                }

        except ValueError as ve:
            logger.error(f"Validation error deleting player-team relationship {relationship_id}: {str(ve)}")
            return {
                "status": SERVER_STATUS.BAD_REQUEST.CODE,
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            logger.error(f"Error deleting player-team relationship {relationship_id}: {str(e)}")
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

# Create a global instance
player_team_delete_handler = PlayerTeamDeleteHandler()
