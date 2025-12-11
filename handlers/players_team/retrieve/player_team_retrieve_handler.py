from bson import ObjectId
from typing import Dict, Any, List
from classes.database.database import mongodb_service
from classes.database.json_storage import json_storage
from classes.database.sync_service import sync_service
from classes.player_team.player_team import PlayerTeam
from classes.team.team import Team
from classes.player.Player import Player
from constants.response_constants import ServerStatus
import logging

logger = logging.getLogger(__name__)
SERVER_STATUS = ServerStatus()

class PlayerTeamRetrieveHandler:
    def __init__(self):
        self.collection = None
        self.players_collection = None
        self.teams_collection = None
        self._update_collections()

    def _update_collections(self):
        """Update collection references if not offline"""
        if not mongodb_service.is_offline:
            self.collection = mongodb_service.get_players_team_collection()
            self.players_collection = mongodb_service.get_players_collection()
            self.teams_collection = mongodb_service.get_teams_collection()

    def get_all_player_teams(self) -> Dict[str, Any]:
        """Get all player-team relationships using the PlayerTeam class array functionality"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collections()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()

            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info("Using local JSON storage for player-team relationships")
                relationships_data = json_storage.get_all_players_team()

                # Return simplified data in offline mode
                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode)",
                    "data": relationships_data
                }

            # Get all documents from MongoDB
            relationships_data = list(self.collection.find())

            # Create a PlayerTeam array instance
            player_teams_array = PlayerTeam()  # This creates an array instance

            # Convert each MongoDB document to PlayerTeam object and add to array
            for rel_doc in relationships_data:
                # Get player and team data
                player_doc = self.players_collection.find_one({"_id": rel_doc["player_id"]})
                team_doc = self.teams_collection.find_one({"_id": rel_doc["team_id"]})

                if player_doc and team_doc:
                    # Create Player and Team instances
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

                    # Create Player array and add player using your class methods
                    players_array = Player()
                    players_array.add(player)

                    # Create PlayerTeam instance using your existing class
                    player_team = PlayerTeam(team=team, players=players_array)

                    # Add relationship metadata
                    player_team._id = str(rel_doc["_id"])
                    player_team.position = rel_doc.get("position")
                    player_team.jersey_number = rel_doc.get("jersey_number")
                    player_team.start_date = rel_doc.get("start_date")
                    player_team.end_date = rel_doc.get("end_date")
                    player_team.is_active = rel_doc.get("is_active")

                    player_teams_array.add(player_team)

            # Use your existing dictionary() method from Object class
            player_teams_dict_array = player_teams_array.dictionary()

            # Add relationship metadata to each dictionary
            for i, pt_dict in enumerate(player_teams_dict_array):
                if hasattr(player_teams_array.object_array[i], '_id'):
                    pt_dict["_id"] = player_teams_array.object_array[i]._id
                if hasattr(player_teams_array.object_array[i], 'position'):
                    pt_dict["position"] = player_teams_array.object_array[i].position
                if hasattr(player_teams_array.object_array[i], 'jersey_number'):
                    pt_dict["jersey_number"] = player_teams_array.object_array[i].jersey_number
                if hasattr(player_teams_array.object_array[i], 'start_date'):
                    pt_dict["start_date"] = player_teams_array.object_array[i].start_date
                if hasattr(player_teams_array.object_array[i], 'end_date'):
                    pt_dict["end_date"] = player_teams_array.object_array[i].end_date
                if hasattr(player_teams_array.object_array[i], 'is_active'):
                    pt_dict["is_active"] = player_teams_array.object_array[i].is_active

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": SERVER_STATUS.SUCCESS.MESSAGE,
                "data": player_teams_dict_array
            }

        except Exception as e:
            logger.error(f"Error retrieving player-team relationships: {str(e)}")
            # Fallback to JSON storage
            try:
                logger.info("Falling back to JSON storage due to error")
                relationships_data = json_storage.get_all_players_team()

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode - fallback)",
                    "data": relationships_data
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

    def get_player_team_by_id(self, relationship_id: str) -> Dict[str, Any]:
        """Get a specific player-team relationship by ID using PlayerTeam class"""
        try:
            # Check connection and try to sync if reconnected
            if mongodb_service.check_connection():
                self._update_collections()
                if json_storage.has_data():
                    logger.info("Connection restored - syncing JSON data to MongoDB")
                    sync_service.sync_all_to_mongodb()

            # If offline, use JSON storage
            if mongodb_service.is_offline:
                logger.info(f"Using local JSON storage for player-team {relationship_id}")
                rel_doc = json_storage.get_player_team_by_id(relationship_id)

                if not rel_doc:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Player-team relationship not found"
                    }

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode)",
                    "data": rel_doc
                }

            # Validate ObjectId format
            if not ObjectId.is_valid(relationship_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid relationship ID format"
                }

            # Find relationship in MongoDB
            rel_doc = self.collection.find_one({"_id": ObjectId(relationship_id)})

            if not rel_doc:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Player-team relationship not found"
                }

            # Get player and team data
            player_doc = self.players_collection.find_one({"_id": rel_doc["player_id"]})
            team_doc = self.teams_collection.find_one({"_id": rel_doc["team_id"]})

            if not player_doc or not team_doc:
                return {
                    "status": SERVER_STATUS.NOT_FOUND.CODE,
                    "message": "Associated player or team not found"
                }

            # Create Player and Team instances
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

            # Create Player array and add player using your class methods
            players_array = Player()
            players_array.add(player)

            # Create PlayerTeam instance using your existing class
            player_team = PlayerTeam(team=team, players=players_array)

            # Use your existing dictionary_team() method from PlayerTeam class
            player_team_dict = player_team.dictionary_team()

            # Add relationship metadata
            player_team_dict["_id"] = str(rel_doc["_id"])
            player_team_dict["position"] = rel_doc.get("position")
            player_team_dict["jersey_number"] = rel_doc.get("jersey_number")
            player_team_dict["start_date"] = rel_doc.get("start_date")
            player_team_dict["end_date"] = rel_doc.get("end_date")
            player_team_dict["is_active"] = rel_doc.get("is_active")

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": SERVER_STATUS.SUCCESS.MESSAGE,
                "data": player_team_dict
            }

        except Exception as e:
            logger.error(f"Error retrieving player-team relationship {relationship_id}: {str(e)}")
            # Fallback to JSON storage
            try:
                logger.info("Falling back to JSON storage due to error")
                rel_doc = json_storage.get_player_team_by_id(relationship_id)

                if not rel_doc:
                    return {
                        "status": SERVER_STATUS.NOT_FOUND.CODE,
                        "message": "Player-team relationship not found"
                    }

                return {
                    "status": SERVER_STATUS.SUCCESS.CODE,
                    "message": SERVER_STATUS.SUCCESS.MESSAGE + " (offline mode - fallback)",
                    "data": rel_doc
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                    "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
                }

    def get_players_by_team(self, team_id: str) -> Dict[str, Any]:
        """Get all players in a specific team using Team and Player classes"""
        try:
            if not ObjectId.is_valid(team_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid team ID format"
                }

            # Verify team exists and create Team instance
            team_doc = self.teams_collection.find_one({"_id": ObjectId(team_id)})
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

            # Find all relationships for this team
            relationships = list(self.collection.find({"team_id": ObjectId(team_id)}))

            # Create Players array using your class methods
            players_array = Player()

            for rel in relationships:
                # Get player data
                player_doc = self.players_collection.find_one({"_id": rel["player_id"]})
                if player_doc:
                    player = Player(
                        name=player_doc.get("name"),
                        age=player_doc.get("age"),
                        number=player_doc.get("number"),
                        nationality=player_doc.get("nationality"),
                        position=player_doc.get("position")
                    )

                    # Add relationship metadata to player
                    player._id = str(rel["_id"])
                    player.relationship_position = rel.get("position")
                    player.jersey_number = rel.get("jersey_number")
                    player.start_date = rel.get("start_date")
                    player.end_date = rel.get("end_date")
                    player.is_active = rel.get("is_active")

                    players_array.add(player)

            # Create PlayerTeam instance using your existing classes
            player_team = PlayerTeam(team=team, players=players_array)

            # Use your existing dictionary_team() method
            result_dict = player_team.dictionary_team()

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": SERVER_STATUS.SUCCESS.MESSAGE,
                "data": result_dict
            }

        except Exception as e:
            logger.error(f"Error retrieving players for team {team_id}: {str(e)}")
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

    def get_teams_by_player(self, player_id: str) -> Dict[str, Any]:
        """Get all teams for a specific player using Team and Player classes"""
        try:
            if not ObjectId.is_valid(player_id):
                return {
                    "status": SERVER_STATUS.BAD_REQUEST.CODE,
                    "message": "Invalid player ID format"
                }

            # Verify player exists and create Player instance
            player_doc = self.players_collection.find_one({"_id": ObjectId(player_id)})
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

            # Find all relationships for this player
            relationships = list(self.collection.find({"player_id": ObjectId(player_id)}))

            # Create PlayerTeam array using your class methods
            player_teams_array = PlayerTeam()

            for rel in relationships:
                # Get team data
                team_doc = self.teams_collection.find_one({"_id": rel["team_id"]})
                if team_doc:
                    team = Team(
                        name=team_doc.get("name"),
                        sport=team_doc.get("sport"),
                        city=team_doc.get("city")
                    )

                    # Create Player array with single player using your class methods
                    single_player_array = Player()
                    single_player_array.add(player)

                    # Create PlayerTeam instance
                    player_team = PlayerTeam(team=team, players=single_player_array)

                    # Add relationship metadata
                    player_team._id = str(rel["_id"])
                    player_team.position = rel.get("position")
                    player_team.jersey_number = rel.get("jersey_number")
                    player_team.start_date = rel.get("start_date")
                    player_team.end_date = rel.get("end_date")
                    player_team.is_active = rel.get("is_active")

                    player_teams_array.add(player_team)

            # Use your existing dictionary() method from Object class
            result_dict = player_teams_array.dictionary()

            return {
                "status": SERVER_STATUS.SUCCESS.CODE,
                "message": SERVER_STATUS.SUCCESS.MESSAGE,
                "data": result_dict
            }

        except Exception as e:
            logger.error(f"Error retrieving teams for player {player_id}: {str(e)}")
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

# Create a global instance
player_team_retrieve_handler = PlayerTeamRetrieveHandler()
