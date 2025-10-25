from typing import Dict, Any
from classes.database.database import mongodb_service
from classes.player.Player import Player
from classes.player.PlayerInterface import PlayerRequest
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class PlayerAddHandler:
    def __init__(self):
        self.collection = mongodb_service.get_players_collection()

    def add_player(self, player_request: PlayerRequest) -> Dict[str, Any]:
        """Add a new player using the Player class"""
        try:
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
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

# Create a global instance
player_add_handler = PlayerAddHandler()
