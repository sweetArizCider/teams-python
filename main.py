from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from routes.player.player_route import router as player_router
from routes.players_team.players_team_route import router as players_team_router
from routes.team.team_router import router as team_router

app = FastAPI()
router = APIRouter()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(player_router, prefix="/player")
app.include_router(players_team_router, prefix='/players_teams')
app.include_router(team_router, prefix='/teams')
