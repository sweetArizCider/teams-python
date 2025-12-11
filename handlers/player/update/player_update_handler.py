from bson import ObjectId
from typing import Dict, Any
from classes.database.database import mongodb_service
from classes.database.json_storage import json_storage
from classes.database.sync_service import sync_service
from classes.player.Player import Player
from classes.player.PlayerInterface import PlayerRequest
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class PlayerUpdateHandler:
    def __init__(self):
        self.collection = None
        self._update_collection()

    def _update_collection(self):
        """Update collection reference if not offline"""
        if not mongodb_service.is_offline:
            self.collection = mongodb_service.get_players_collection()

    def update_player(self, player_id: str, player_request: PlayerRequest) -> Dict[str, Any]:
        """Update a player using the Player class"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collection()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()

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

            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info(f"Using local JSON storage to update player {player_id}")
                success = json_storage.update_player(player_id, update_data)

                if not success:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Player not found"
                    }

                updated_player_doc = json_storage.get_player_by_id(player_id)
                updated_player_doc["_id"] = str(updated_player_doc["_id"])

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": "Player updated successfully (offline mode - will sync when online)",
                    "data": updated_player_doc
                }

            # Validate ObjectId format
            if not ObjectId.is_valid(player_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid player ID format"
                }

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
            # On error, try JSON storage as fallback
            try:
                logger.info("Falling back to JSON storage due to error")
                updated_player = Player(
                    name=player_request.name,
                    age=player_request.age,
                    number=player_request.number,
                    nationality=player_request.nationality,
                    position=player_request.position
                )
                update_data = updated_player.dictionary()
                success = json_storage.update_player(player_id, update_data)

                if not success:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Player not found"
                    }

                updated_player_doc = json_storage.get_player_by_id(player_id)
                updated_player_doc["_id"] = str(updated_player_doc["_id"])

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": "Player updated successfully (offline mode - will sync when online)",
                    "data": updated_player_doc
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

# Create a global instance
player_update_handler = PlayerUpdateHandler()
