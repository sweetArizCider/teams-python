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

class PlayerRetrieveHandler:
    def __init__(self):
        self.collection = None
        self._update_collection()
    
    def _update_collection(self):
        """Update collection reference if not offline"""
        if not mongodb_service.is_offline:
            self.collection = mongodb_service.get_players_collection()

    def get_all_players(self) -> Dict[str, Any]:
        """Get all players using the Player class array functionality"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collection()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()
            
            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info("Using local JSON storage for players")
                players_data = json_storage.get_all_players()
                
                # Create a Player array instance
                players_array = Player()
                
                for player_doc in players_data:
                    player = Player(
                        name=player_doc.get("name"),
                        age=player_doc.get("age"),
                        number=player_doc.get("number"),
                        nationality=player_doc.get("nationality"),
                        position=player_doc.get("position")
                    )
                    player._id = player_doc["_id"]
                    players_array.add(player)
                
                players_dict_array = players_array.dictionary()
                for i, player_dict in enumerate(players_dict_array):
                    if hasattr(players_array.object_array[i], '_id'):
                        player_dict["_id"] = players_array.object_array[i]._id
                
                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode)",
                    "data": players_dict_array
                }
            
            # Get all documents from MongoDB
            players_data = list(self.collection.find())

            # Create a Player array instance
            players_array = Player()  # This creates an array instance

            # Convert each MongoDB document to Player object and add to array
            for player_doc in players_data:
                # Convert ObjectId to string for the document
                player_doc["_id"] = str(player_doc["_id"])

                # Create Player instance from MongoDB data
                player = Player(
                    name=player_doc.get("name"),
                    age=player_doc.get("age"),
                    number=player_doc.get("number"),
                    nationality=player_doc.get("nationality"),
                    position=player_doc.get("position")
                )

                # Add the _id to the player object for response
                player._id = player_doc["_id"]

                players_array.add(player)

            # Use your existing dictionary() method from Object class
            players_dict_array = players_array.dictionary()

            # Add _id to each player dictionary
            for i, player_dict in enumerate(players_dict_array):
                if hasattr(players_array.object_array[i], '_id'):
                    player_dict["_id"] = players_array.object_array[i]._id

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": SERVER_STATUS.SUCCESS.MESSAGE,
                "data": players_dict_array
            }

        except Exception as e:
            logger.error(f"Error retrieving players: {str(e)}")
            # On error, try JSON storage as fallback
            try:
                logger.info("Falling back to JSON storage due to error")
                players_data = json_storage.get_all_players()
                players_array = Player()
                
                for player_doc in players_data:
                    player = Player(
                        name=player_doc.get("name"),
                        age=player_doc.get("age"),
                        number=player_doc.get("number"),
                        nationality=player_doc.get("nationality"),
                        position=player_doc.get("position")
                    )
                    player._id = player_doc["_id"]
                    players_array.add(player)
                
                players_dict_array = players_array.dictionary()
                for i, player_dict in enumerate(players_dict_array):
                    if hasattr(players_array.object_array[i], '_id'):
                        player_dict["_id"] = players_array.object_array[i]._id
                
                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode - fallback)",
                    "data": players_dict_array
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

    def get_player_by_id(self, player_id: str) -> Dict[str, Any]:
        """Get a specific player by ID using the Player class"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collection()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()
            
            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info(f"Using local JSON storage for player {player_id}")
                player_doc = json_storage.get_player_by_id(player_id)
                
                if not player_doc:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Player not found"
                    }
                
                player = Player(
                    name=player_doc.get("name"),
                    age=player_doc.get("age"),
                    number=player_doc.get("number"),
                    nationality=player_doc.get("nationality"),
                    position=player_doc.get("position")
                )
                
                player_dict = player.dictionary()
                player_dict["_id"] = player_doc["_id"]
                
                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode)",
                    "data": player_dict
                }
            
            # Validate ObjectId format
            if not ObjectId.is_valid(player_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid player ID format"
                }

            # Find player in MongoDB
            player_doc = self.collection.find_one({"_id": ObjectId(player_id)})

            if not player_doc:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Player not found"
                }

            # Convert ObjectId to string
            player_doc["_id"] = str(player_doc["_id"])

            # Create Player instance from MongoDB data
            player = Player(
                name=player_doc.get("name"),
                age=player_doc.get("age"),
                number=player_doc.get("number"),
                nationality=player_doc.get("nationality"),
                position=player_doc.get("position")
            )

            # Use your existing dictionary() method from Object class
            player_dict = player.dictionary()
            player_dict["_id"] = player_doc["_id"]

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": SERVER_STATUS.SUCCESS.MESSAGE,
                "data": player_dict
            }

        except ValueError as ve:
            logger.error(f"Validation error retrieving player {player_id}: {str(ve)}")
            return {
                "status": SERVER_STATUS.BAD_REQUEST.CODE,
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            logger.error(f"Error retrieving player {player_id}: {str(e)}")
            # On error, try JSON storage as fallback
            try:
                logger.info("Falling back to JSON storage due to error")
                player_doc = json_storage.get_player_by_id(player_id)
                
                if not player_doc:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Player not found"
                    }
                
                player = Player(
                    name=player_doc.get("name"),
                    age=player_doc.get("age"),
                    number=player_doc.get("number"),
                    nationality=player_doc.get("nationality"),
                    position=player_doc.get("position")
                )
                
                player_dict = player.dictionary()
                player_dict["_id"] = player_doc["_id"]
                
                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode - fallback)",
                    "data": player_dict
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

# Create a global instance
player_retrieve_handler = PlayerRetrieveHandler()
