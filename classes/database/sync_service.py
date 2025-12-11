from classes.database.database import mongodb_service
from classes.database.json_storage import json_storage
import logging

logger = logging.getLogger(__name__)

class SyncService:
    """Service to sync JSON data to MongoDB when connection is restored"""

    def sync_all_to_mongodb(self) -> dict:
        """Sync all JSON data to MongoDB and delete JSON files if successful"""
        if mongodb_service.is_offline:
            logger.warning("Cannot sync - MongoDB is offline")
            return {
                "success": False,
                "message": "MongoDB connection not available"
            }

        if not json_storage.has_data():
            logger.info("No JSON data to sync")
            return {
                "success": True,
                "message": "No data to sync"
            }

        results = {
            "players": {"synced": 0, "errors": 0},
            "teams": {"synced": 0, "errors": 0},
            "players_team": {"synced": 0, "errors": 0}
        }

        try:
            # Sync players
            players = json_storage.get_all_players()
            for player in players:
                try:
                    # Remove local ID and timestamps
                    player_data = {k: v for k, v in player.items()
                                   if k not in ["_id", "created_at", "updated_at"]
                                   and not k.startswith("local_")}

                    # Insert into MongoDB
                    mongodb_service.get_players_collection().insert_one(player_data)
                    results["players"]["synced"] += 1
                    logger.info(f"Synced player: {player.get('name')}")
                except Exception as e:
                    logger.error(f"Error syncing player {player.get('name')}: {str(e)}")
                    results["players"]["errors"] += 1

            # Sync teams
            teams = json_storage.get_all_teams()
            for team in teams:
                try:
                    # Remove local ID and timestamps
                    team_data = {k: v for k, v in team.items()
                                 if k not in ["_id", "created_at", "updated_at"]
                                 and not k.startswith("local_")}

                    # Insert into MongoDB
                    mongodb_service.get_teams_collection().insert_one(team_data)
                    results["teams"]["synced"] += 1
                    logger.info(f"Synced team: {team.get('name')}")
                except Exception as e:
                    logger.error(f"Error syncing team {team.get('name')}: {str(e)}")
                    results["teams"]["errors"] += 1

            # Sync players_team
            players_team = json_storage.get_all_players_team()
            for rel in players_team:
                try:
                    # Remove local ID and timestamps
                    rel_data = {k: v for k, v in rel.items()
                                if k not in ["_id", "created_at", "updated_at"]
                                and not k.startswith("local_")}

                    # Insert into MongoDB
                    mongodb_service.get_players_team_collection().insert_one(rel_data)
                    results["players_team"]["synced"] += 1
                    logger.info(f"Synced player-team relationship")
                except Exception as e:
                    logger.error(f"Error syncing player-team relationship: {str(e)}")
                    results["players_team"]["errors"] += 1

            # If all syncs were successful, clear JSON files
            total_errors = sum(r["errors"] for r in results.values())
            if total_errors == 0:
                json_storage.clear_all()
                logger.info("All data synced successfully - JSON files cleared")

            return {
                "success": total_errors == 0,
                "message": "Sync completed",
                "results": results
            }

        except Exception as e:
            logger.error(f"Error during sync: {str(e)}")
            return {
                "success": False,
                "message": f"Sync failed: {str(e)}",
                "results": results
            }

# Create a global instance
sync_service = SyncService()
