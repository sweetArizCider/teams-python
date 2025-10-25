from pydantic import BaseModel
from typing import Optional, List

class PlayerTeamRequest(BaseModel):
    player_id: str
    team_id: str
    position: Optional[str] = None
    jersey_number: Optional[int] = None
    start_date: Optional[str] = None  # Can be ISO date string
    end_date: Optional[str] = None    # Can be ISO date string
    is_active: Optional[bool] = True

class PlayerTeamArrayRequest(BaseModel):
    is_array: bool = True
    object_array: Optional[List[PlayerTeamRequest]] = []
    player_id: Optional[str] = None
    team_id: Optional[str] = None
    position: Optional[str] = None
    jersey_number: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_active: Optional[bool] = True
