from object import Object

class Team(Object):
  def __init__(
      self,
      name=None,
      sport=None,
      city=None  # optional, default is None
  ):
    is_array = (name is None and sport is None)
    super().__init__(is_array=is_array)

    if not self.is_array:
      if name is None or sport is None:
        raise ValueError("Both 'name' and 'sport' are required for a Team.")
      self.name = name
      self.sport = sport
      self.city = city

  def __str__(self):
    if self.is_array:
      return super().__str__()
    return f"- Team: {self.name}, Sport: {self.sport}, City: {self.city}"

if __name__ == '__main__':
  single_team = Team('Barcelona', 'Soccer', 'Barcelona')
  single_team.to_json_file('single_team.json')

  teams = Team()
  teams.add(Team('Real Madrid', 'Soccer', 'Madrid'))
  teams.add(Team('Atletico Madrid', 'Soccer', 'Madrid'))
  teams.list()
  teams.to_json_file('teams.json')

  team_instance = Team()
  loaded_teams = team_instance.json_to_object('teams.json')
  print("\nLoaded single teams:")
  print(loaded_teams)

  loaded_teams.list()