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

class PlayerTeamAddHandler:
    def __init__(self):
        self.collection = mongodb_service.get_players_team_collection()
        self.players_collection = mongodb_service.get_players_collection()
        self.teams_collection = mongodb_service.get_teams_collection()

    def add_player_team(self, player_team_request: PlayerTeamRequest) -> Dict[str, Any]:
        """Add a new player-team relationship using the PlayerTeam class"""
        try:
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

            # Create Player and Team instances from the found documents
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

            # Create PlayerTeam instance using your existing class
            player_team = PlayerTeam(team=team, players=players_array)

            # For MongoDB storage, we store the relationship data directly (not the full objects)
            # This is because we're storing relationships, not the actual Player/Team objects
            player_team_data = {
                "player_id": ObjectId(player_team_request.player_id),
                "team_id": ObjectId(player_team_request.team_id),
                "position": player_team_request.position,
                "jersey_number": player_team_request.jersey_number,
                "start_date": player_team_request.start_date,
                "end_date": player_team_request.end_date,
                "is_active": player_team_request.is_active
            }

            # Insert into MongoDB
            result = self.collection.insert_one(player_team_data)

            # Get the created relationship from MongoDB
            created_relationship = self.collection.find_one({"_id": result.inserted_id})
            created_relationship["_id"] = str(created_relationship["_id"])
            created_relationship["player_id"] = str(created_relationship["player_id"])
            created_relationship["team_id"] = str(created_relationship["team_id"])

            return {
                "status": SERVER_STATUS.CREATED.CODE,
                "message": SERVER_STATUS.CREATED.MESSAGE,
                "data": created_relationship
            }

        except ValueError as ve:
            logger.error(f"Validation error creating player-team relationship: {str(ve)}")
            return {
                "status": SERVER_STATUS.BAD_REQUEST.CODE,
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            logger.error(f"Error creating player-team relationship: {str(e)}")
            return {
                "status": SERVER_STATUS.INTERNAL_SERVER_ERROR.CODE,
                "message": f"{SERVER_STATUS.INTERNAL_SERVER_ERROR.MESSAGE}: {str(e)}"
            }

# Create a global instance
player_team_add_handler = PlayerTeamAddHandler()
