from object import Object

class Team(Object):
  def __init__(
      self, 
      name = None, 
      sport = None,  
      city = None, #optional
    ):
    if not (name is None or sport is None):
      self.name = name
      self.sport = sport
      self.city = city if city is not None else None
    else:
      super().__init__()

  def __str__(self):
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
  teams_array.list()