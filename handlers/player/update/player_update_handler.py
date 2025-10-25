from bson import ObjectId
from typing import Dict, Any
from classes.database.database import mongodb_service
from classes.player.Player import Player
from classes.player.PlayerInterface import PlayerRequest
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class PlayerUpdateHandler:
    def __init__(self):
        self.collection = mongodb_service.get_players_collection()

    def update_player(self, player_id: str, player_request: PlayerRequest) -> Dict[str, Any]:
        """Update a player using the Player class"""
        try:
            # Validate ObjectId format
            if not ObjectId.is_valid(player_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid player ID format"
                }

            # Create Player instance with updated data
            updated_player = Player(
                name=player_request.name,
                age=player_request.age,
                number=player_request.number,
                nationality=player_request.nationality,
                position=player_request.position
            )

            # Use your existing dictionary() method from Object class
            update_data = updated_player.dictionary()

            # Update in MongoDB
            result = self.collection.update_one(
                {"_id": ObjectId(player_id)},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Player not found"
                }

            # Get the updated player from MongoDB
            updated_player_doc = self.collection.find_one({"_id": ObjectId(player_id)})
            updated_player_doc["_id"] = str(updated_player_doc["_id"])

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": "Player updated successfully",
                "data": updated_player_doc
            }

        except ValueError as ve:
            logger.error(f"Validation error updating player {player_id}: {str(ve)}")
            return {
                "status": SERVER_STATUS.BAD_REQUEST.CODE,
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            logger.error(f"Error updating player {player_id}: {str(e)}")
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

# Create a global instance
player_update_handler = PlayerUpdateHandler()
