from pydantic import BaseModel
from typing import Optional, List

class TeamRequest(BaseModel):
    name: str
    sport: str
    city: Optional[str] = None

class TeamArrayRequest(BaseModel):
    is_array: bool = True
    object_array: Optional[List[TeamRequest]] = []
    name: Optional[str] = None
    sport: Optional[str] = None
    city: Optional[str] = None
