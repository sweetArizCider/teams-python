class Team:
  def __init__(
      self, 
      name = None, 
      sport = None,  
      city = None, #optional
    ):
    # Name and Sport are required to create an object!!
    if not (name == None or sport == None):
      self.name = name
      self.sport = sport
      self.city = city
      self.is_array = False
      return
    
    self.is_array = True
    self.object_array = []
    self.index = 0
    
  def __str__(self):
    return f"Team: {self.name} \nSport: {self.sport} \nCity: {self.city}"

  def add_team(self, team):
    if not self.is_array:
      return print("This is not an Array of teams!, team not added")
    team.index = len(self.teams)
    self.teams.append(team)
    return print("Team added!")

  def list_teams(self):
    if not self.is_array:
      return print("This is not an Array of teams!")
    for team in self.teams:
      print(f"\n{team}")
    return

  def update_team(self, index, new_name = None, new_sport = None, new_city = None):
    if index == None:
      return print("Index is required!!")
    if not self.is_array:
      return print("This is not an array of teams!!")
    team = self.teams[index]

    if new_name:
      team.name = new_name
    if new_sport:
      team.sport = new_sport
    if new_city:
      team.city = new_city
    return print("Team updated!")

  def remove_team(self, index):
    if index == None:
      return print("Index is required!!")
    if not self.is_array:
      return print("This is not an array of teams!!")
    self.teams.pop(index)
    return print("Team removed!")

if __name__ == '__main__':

  # Creating a single team
  print("=================SINGLE TEAM=================")
  single_team = Team('Cruz Azul', 'Soccer', 'Mexico City')
  single_team2 = Team('Santos Laguna', 'Soccer', 'Torreon')
  single_team3 = Team('Toluca', 'Soccer', 'Edo Mex')
  single_team4 = Team('Vikings', 'Football', 'Minesotta')
  print(single_team)


  print("=================TEAMS ARRAY=================")
  teams_array = Team()
  teams_array.add_team(single_team)
  teams_array.add_team(single_team2)
  teams_array.add_team(single_team3)
  teams_array.add_team(single_team4)

  teams_array.update_team(index=0, new_name='Cruz Azul FC')
  teams_array.update_team(index=3, new_city='Minneapolis')
  teams_array.remove_team(index=2)
  teams_array.list_teams()