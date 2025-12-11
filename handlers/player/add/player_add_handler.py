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

class PlayerAddHandler:
    def __init__(self):
        self.collection = None
        self._update_collection()

    def _update_collection(self):
        """Update collection reference if not offline"""
        if not mongodb_service.is_offline:
            self.collection = mongodb_service.get_players_collection()

    def add_player(self, player_request: PlayerRequest) -> Dict[str, Any]:
        """Add a new player using the Player class"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collection()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()

            # Create Player instance using the existing Player class
            player = Player(
                name=player_request.name,
                age=player_request.age,
                number=player_request.number,
                nationality=player_request.nationality,
                position=player_request.position
            )

            # Use your existing dictionary() method from Object class
            player_data = player.dictionary()

            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info("Using local JSON storage to add player")
                created_player = json_storage.add_player(player_data)

                return {
                    "status": SERVER_STATUS.CREATED.CODE,
                    "message": SERVER_STATUS.CREATED.MESSAGE + " (offline mode - will sync when online)",
                    "data": created_player
                }

            # Insert into MongoDB
            result = self.collection.insert_one(player_data)

            # Get the created player from MongoDB
            created_player = self.collection.find_one({"_id": result.inserted_id})
            created_player["_id"] = str(created_player["_id"])  # Convert ObjectId to string

            return {
                "status": SERVER_STATUS.CREATED.CODE,
                "message": SERVER_STATUS.CREATED.MESSAGE,
                "data": created_player
            }

        except ValueError as ve:
            logger.error(f"Validation error creating player: {str(ve)}")
            return {
                "status": SERVER_STATUS.BAD_REQUEST.CODE,
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            logger.error(f"Error creating player: {str(e)}")
            # On error, try JSON storage as fallback
            try:
                logger.info("Falling back to JSON storage due to error")
                player = Player(
                    name=player_request.name,
                    age=player_request.age,
                    number=player_request.number,
                    nationality=player_request.nationality,
                    position=player_request.position
                )
                player_data = player.dictionary()
                created_player = json_storage.add_player(player_data)

                return {
                    "status": SERVER_STATUS.CREATED.CODE,
                    "message": SERVER_STATUS.CREATED.MESSAGE + " (offline mode - will sync when online)",
                    "data": created_player
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

# Create a global instance
player_add_handler = PlayerAddHandler()
