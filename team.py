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
  # Creating a single team
  #"=================SINGLE TEAM=================")
  single_team = Team('Cruz Azul', 'Soccer', 'Mexico City')
  single_team2 = Team('Santos Laguna', 'Soccer', 'Torreon')
  single_team3 = Team('Toluca', 'Soccer', 'Edo Mex')
  single_team4 = Team('Vikings', 'Football', 'Minesotta')

  #"=================TEAMS ARRAY=================")
  teams_array = Team()
  teams_array.add(single_team)
  teams_array.add(single_team2)
  teams_array.add(single_team3)
  teams_array.add(single_team4)

  # updates Toluca to Pumas
  teams_array.update(index=2, object_element=Team('Pumas', 'Soccer', 'CDMX'))
  # removes Vikings
  teams_array.remove(index=3)
  # lists all teams
  teams_array.list()
  # print how many teams are in the array
  print(teams_array)
  print("=================TEAMS ARRAY=================")
  print(teams_array.dictionary())
  print(single_team.dictionary())
