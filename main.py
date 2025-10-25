from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from routes.player.player_route import router as player_router
from routes.players_team.players_team_route import router as players_team_router
from routes.team.team_router import router as team_router

app = FastAPI()
router = APIRouter()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(player_router, prefix="/players")
app.include_router(players_team_router, prefix='/players_team')
app.include_router(team_router, prefix='/teams')

@app.get("/")
async def root():
    return {"message": "Teams Python MongoDB API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
