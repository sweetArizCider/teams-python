from pydantic import BaseModel
from typing import Optional, List

class PlayerRequest(BaseModel):
  name: str
  age: int
  number: Optional[int] = None
  nationality: Optional[str] = None
  position: Optional[str] = None

class PlayerArrayRequest(BaseModel):
  is_array: bool = True
  object_array: Optional[List[PlayerRequest]] = []
  name: Optional[str] = None
  age: Optional[int] = None
  number: Optional[int] = None
  nationality: Optional[str] = None
  position: Optional[str] = None