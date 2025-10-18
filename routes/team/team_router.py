from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def team():
    return {"message": "Team Route"}