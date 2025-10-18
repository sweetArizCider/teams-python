from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_players_team():
    return {"message": "Players Team Route"}