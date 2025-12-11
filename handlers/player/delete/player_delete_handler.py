from bson import ObjectId
from typing import Dict, Any
from classes.database.database import mongodb_service
from classes.database.json_storage import json_storage
from classes.database.sync_service import sync_service
from classes.player.Player import Player
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class PlayerDeleteHandler:
    def __init__(self):
        self.collection = None
        self._update_collection()

    def _update_collection(self):
        """Update collection reference if not offline"""
        if not mongodb_service.is_offline:
            self.collection = mongodb_service.get_players_collection()

    def delete_player(self, player_id: str) -> Dict[str, Any]:
        """Delete a player using validation from Player class"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collection()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()

            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info(f"Using local JSON storage to delete player {player_id}")

                # Get player before deletion for response
                existing_player = json_storage.get_player_by_id(player_id)
                if not existing_player:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Player not found"
                    }

                player_name = existing_player.get("name")
                success = json_storage.delete_player(player_id)

                if not success:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Player not found or already deleted"
                    }

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": f"Player '{player_name}' deleted successfully (offline mode)"
                }

            # Validate ObjectId format
            if not ObjectId.is_valid(player_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid player ID format"
                }

            # Check if player exists before deletion (optional but good practice)
            existing_player = self.collection.find_one({"_id": ObjectId(player_id)})
            if not existing_player:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Player not found"
                }

            # Create Player instance to log what's being deleted
            player_to_delete = Player(
                name=existing_player.get("name"),
                age=existing_player.get("age"),
                number=existing_player.get("number"),
                nationality=existing_player.get("nationality"),
                position=existing_player.get("position")
            )

            # Log the deletion for audit purposes
            logger.info(f"Deleting player: {player_to_delete}")

            # Delete from MongoDB
            result = self.collection.delete_one({"_id": ObjectId(player_id)})

            if result.deleted_count == 0:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Player not found or already deleted"
                }

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": f"Player '{player_to_delete.name}' deleted successfully"
            }

        except ValueError as ve:
            logger.error(f"Validation error deleting player {player_id}: {str(ve)}")
            return {
                "status": SERVER_STATUS.BAD_REQUEST.CODE,
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            logger.error(f"Error deleting player {player_id}: {str(e)}")
            # On error, try JSON storage as fallback
            try:
                logger.info("Falling back to JSON storage due to error")
                existing_player = json_storage.get_player_by_id(player_id)
                if not existing_player:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Player not found"
                    }

                player_name = existing_player.get("name")
                success = json_storage.delete_player(player_id)

                if not success:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Player not found or already deleted"
                    }

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": f"Player '{player_name}' deleted successfully (offline mode)"
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

# Create a global instance
player_delete_handler = PlayerDeleteHandler()
