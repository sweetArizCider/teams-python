import json
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class JSONStorage:
    """Local JSON file storage for offline mode"""

    def __init__(self, storage_dir: str = "local_storage"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

        self.players_file = self.storage_dir / "players.json"
        self.teams_file = self.storage_dir / "teams.json"
        self.players_team_file = self.storage_dir / "players_team.json"
        self.counter_file = self.storage_dir / "id_counter.json"

        # Initialize counter for generating IDs
        self._init_counter()

    def _init_counter(self):
        """Initialize ID counter if not exists"""
        if not self.counter_file.exists():
            counter_data = {
                "players": 0,
                "teams": 0,
                "players_team": 0
            }
            self._write_json(self.counter_file, counter_data)

    def _read_json(self, file_path: Path) -> Any:
        """Read JSON file"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return [] if file_path.name != "id_counter.json" else {}
        except Exception as e:
            logger.error(f"Error reading {file_path}: {str(e)}")
            return [] if file_path.name != "id_counter.json" else {}

    def _write_json(self, file_path: Path, data: Any):
        """Write JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error writing to {file_path}: {str(e)}")
            raise

    def _generate_id(self, collection: str) -> str:
        """Generate unique ID for collection"""
        counter_data = self._read_json(self.counter_file)
        counter_data[collection] = counter_data.get(collection, 0) + 1
        self._write_json(self.counter_file, counter_data)
        return f"local_{collection}_{counter_data[collection]}"

    # Player operations
    def get_all_players(self) -> List[Dict[str, Any]]:
        """Get all players from JSON file"""
        return self._read_json(self.players_file)

    def get_player_by_id(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Get player by ID from JSON file"""
        players = self.get_all_players()
        for player in players:
            if player.get("_id") == player_id:
                return player
        return None

    def add_player(self, player_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add player to JSON file"""
        players = self.get_all_players()
        player_data["_id"] = self._generate_id("players")
        player_data["created_at"] = datetime.now().isoformat()
        players.append(player_data)
        self._write_json(self.players_file, players)
        return player_data

    def update_player(self, player_id: str, player_data: Dict[str, Any]) -> bool:
        """Update player in JSON file"""
        players = self.get_all_players()
        for i, player in enumerate(players):
            if player.get("_id") == player_id:
                player_data["_id"] = player_id
                player_data["updated_at"] = datetime.now().isoformat()
                players[i] = player_data
                self._write_json(self.players_file, players)
                return True
        return False

    def delete_player(self, player_id: str) -> bool:
        """Delete player from JSON file"""
        players = self.get_all_players()
        updated_players = [p for p in players if p.get("_id") != player_id]
        if len(updated_players) < len(players):
            self._write_json(self.players_file, updated_players)
            return True
        return False

    # Team operations
    def get_all_teams(self) -> List[Dict[str, Any]]:
        """Get all teams from JSON file"""
        return self._read_json(self.teams_file)

    def get_team_by_id(self, team_id: str) -> Optional[Dict[str, Any]]:
        """Get team by ID from JSON file"""
        teams = self.get_all_teams()
        for team in teams:
            if team.get("_id") == team_id:
                return team
        return None

    def add_team(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add team to JSON file"""
        teams = self.get_all_teams()
        team_data["_id"] = self._generate_id("teams")
        team_data["created_at"] = datetime.now().isoformat()
        teams.append(team_data)
        self._write_json(self.teams_file, teams)
        return team_data

    def update_team(self, team_id: str, team_data: Dict[str, Any]) -> bool:
        """Update team in JSON file"""
        teams = self.get_all_teams()
        for i, team in enumerate(teams):
            if team.get("_id") == team_id:
                team_data["_id"] = team_id
                team_data["updated_at"] = datetime.now().isoformat()
                teams[i] = team_data
                self._write_json(self.teams_file, teams)
                return True
        return False

    def delete_team(self, team_id: str) -> bool:
        """Delete team from JSON file"""
        teams = self.get_all_teams()
        updated_teams = [t for t in teams if t.get("_id") != team_id]
        if len(updated_teams) < len(teams):
            self._write_json(self.teams_file, updated_teams)
            return True
        return False

    # PlayerTeam operations
    def get_all_players_team(self) -> List[Dict[str, Any]]:
        """Get all player-team relationships from JSON file"""
        return self._read_json(self.players_team_file)

    def get_player_team_by_id(self, relationship_id: str) -> Optional[Dict[str, Any]]:
        """Get player-team relationship by ID from JSON file"""
        relationships = self.get_all_players_team()
        for rel in relationships:
            if rel.get("_id") == relationship_id:
                return rel
        return None

    def add_player_team(self, relationship_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add player-team relationship to JSON file"""
        relationships = self.get_all_players_team()
        relationship_data["_id"] = self._generate_id("players_team")
        relationship_data["created_at"] = datetime.now().isoformat()
        relationships.append(relationship_data)
        self._write_json(self.players_team_file, relationships)
        return relationship_data

    def update_player_team(self, relationship_id: str, relationship_data: Dict[str, Any]) -> bool:
        """Update player-team relationship in JSON file"""
        relationships = self.get_all_players_team()
        for i, rel in enumerate(relationships):
            if rel.get("_id") == relationship_id:
                relationship_data["_id"] = relationship_id
                relationship_data["updated_at"] = datetime.now().isoformat()
                relationships[i] = relationship_data
                self._write_json(self.players_team_file, relationships)
                return True
        return False

    def delete_player_team(self, relationship_id: str) -> bool:
        """Delete player-team relationship from JSON file"""
        relationships = self.get_all_players_team()
        updated_relationships = [r for r in relationships if r.get("_id") != relationship_id]
        if len(updated_relationships) < len(relationships):
            self._write_json(self.players_team_file, updated_relationships)
            return True
        return False

    def clear_all(self):
        """Clear all JSON files"""
        for file in [self.players_file, self.teams_file, self.players_team_file]:
            if file.exists():
                file.unlink()
                logger.info(f"Deleted {file}")

    def has_data(self) -> bool:
        """Check if there's any data in JSON files"""
        return (
            (self.players_file.exists() and len(self.get_all_players()) > 0) or
            (self.teams_file.exists() and len(self.get_all_teams()) > 0) or
            (self.players_team_file.exists() and len(self.get_all_players_team()) > 0)
        )

# Create a global instance
json_storage = JSONStorage()
