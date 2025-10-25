# Insomnia REST API Testing Examples for Teams-Python MongoDB API

## Base URL
```
http://localhost:8000
```

## 1. PLAYERS ENDPOINTS

### GET All Players
```
Method: GET
URL: http://localhost:8000/players/
Headers: 
  Content-Type: application/json
```

### GET Player by ID
```
Method: GET
URL: http://localhost:8000/players/507f1f77bcf86cd799439011
Headers: 
  Content-Type: application/json
```

### POST Create Player
```
Method: POST
URL: http://localhost:8000/players/
Headers: 
  Content-Type: application/json
Body (JSON):
{
  "name": "Lionel Messi",
  "age": 36,
  "number": 10,
  "nationality": "Argentina",
  "position": "Forward"
}
```

### POST Create Another Player
```
Method: POST
URL: http://localhost:8000/players/
Headers: 
  Content-Type: application/json
Body (JSON):
{
  "name": "Cristiano Ronaldo",
  "age": 38,
  "number": 7,
  "nationality": "Portugal",
  "position": "Forward"
}
```

### PUT Update Player
```
Method: PUT
URL: http://localhost:8000/players/{player_id_from_create_response}
Headers: 
  Content-Type: application/json
Body (JSON):
{
  "name": "Lionel Messi",
  "age": 37,
  "number": 10,
  "nationality": "Argentina",
  "position": "Right Winger"
}
```

### DELETE Player
```
Method: DELETE
URL: http://localhost:8000/players/{player_id_from_create_response}
Headers: 
  Content-Type: application/json
```

## 2. TEAMS ENDPOINTS

### GET All Teams
```
Method: GET
URL: http://localhost:8000/teams/
Headers: 
  Content-Type: application/json
```

### GET Team by ID
```
Method: GET
URL: http://localhost:8000/teams/507f1f77bcf86cd799439022
Headers: 
  Content-Type: application/json
```

### POST Create Team
```
Method: POST
URL: http://localhost:8000/teams/
Headers: 
  Content-Type: application/json
Body (JSON):
{
  "name": "FC Barcelona",
  "sport": "Football",
  "city": "Barcelona"
}
```

### POST Create Another Team
```
Method: POST
URL: http://localhost:8000/teams/
Headers: 
  Content-Type: application/json
Body (JSON):
{
  "name": "Manchester United",
  "sport": "Football",
  "city": "Manchester"
}
```

### PUT Update Team
```
Method: PUT
URL: http://localhost:8000/teams/{team_id_from_create_response}
Headers: 
  Content-Type: application/json
Body (JSON):
{
  "name": "FC Barcelona",
  "sport": "Football",
  "city": "Barcelona, Spain"
}
```

### DELETE Team
```
Method: DELETE
URL: http://localhost:8000/teams/{team_id_from_create_response}
Headers: 
  Content-Type: application/json
```

## 3. PLAYER-TEAM RELATIONSHIPS ENDPOINTS

### GET All Player-Team Relationships
```
Method: GET
URL: http://localhost:8000/players_team/
Headers: 
  Content-Type: application/json
```

### GET Player-Team Relationship by ID
```
Method: GET
URL: http://localhost:8000/players_team/507f1f77bcf86cd799439033
Headers: 
  Content-Type: application/json
```

### POST Create Player-Team Relationship
```
Method: POST
URL: http://localhost:8000/players_team/
Headers: 
  Content-Type: application/json
Body (JSON):
{
  "player_id": "507f1f77bcf86cd799439011",
  "team_id": "507f1f77bcf86cd799439022",
  "position": "Right Winger",
  "jersey_number": 10,
  "start_date": "2023-08-01",
  "end_date": null,
  "is_active": true
}
```

### GET Players by Team
```
Method: GET
URL: http://localhost:8000/players_team/team/{team_id}/players
Headers: 
  Content-Type: application/json
```

### GET Teams by Player
```
Method: GET
URL: http://localhost:8000/players_team/player/{player_id}/teams
Headers: 
  Content-Type: application/json
```

### PUT Update Player-Team Relationship
```
Method: PUT
URL: http://localhost:8000/players_team/{relationship_id}
Headers: 
  Content-Type: application/json
Body (JSON):
{
  "player_id": "507f1f77bcf86cd799439011",
  "team_id": "507f1f77bcf86cd799439022",
  "position": "Center Forward",
  "jersey_number": 10,
  "start_date": "2023-08-01",
  "end_date": "2024-06-30",
  "is_active": false
}
```

### DELETE Player-Team Relationship
```
Method: DELETE
URL: http://localhost:8000/players_team/{relationship_id}
Headers: 
  Content-Type: application/json
```

## TESTING WORKFLOW EXAMPLE

### Step 1: Create Players
1. Create Messi (save the returned ID)
2. Create Ronaldo (save the returned ID)

### Step 2: Create Teams
1. Create Barcelona (save the returned ID)
2. Create Manchester United (save the returned ID)

### Step 3: Create Relationships
1. Assign Messi to Barcelona
2. Assign Ronaldo to Manchester United

### Step 4: Test Queries
1. Get all players in Barcelona team
2. Get all teams for Messi
3. Get all relationships

## SAMPLE RESPONSE FORMATS

### Successful Response
```json
{
  "status": 200,
  "message": "Success",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "name": "Lionel Messi",
    "age": 36,
    "number": 10,
    "nationality": "Argentina",
    "position": "Forward"
  }
}
```

### Error Response
```json
{
  "status": 404,
  "message": "Player not found"
}
```

## NOTES:
- Replace {player_id}, {team_id}, {relationship_id} with actual IDs from responses
- MongoDB ObjectIDs are 24-character hex strings
- All dates should be in ISO format (YYYY-MM-DD)
- Jersey numbers should be integers
- The is_active field is boolean (true/false)
