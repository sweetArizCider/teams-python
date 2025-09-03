
class Team:
  def __init__(self, name: str, sport: str, active: bool = True):
    self.name = name
    self.sport = sport
    self.active = active

  def change_name(self, new_name: str):
    if not new_name:
      return print(f"No team name, no changes!")
    old_team_name = self.name
    self.name = new_name
    return print(f"Name team updated, changed from {old_team_name} to -> {new_name}")

  def change_sport(self, new_sport: str):
    if not new_sport:
      return
    self.sport = new_sport

  def desactive(self):
    self.active = False

  def activate(self):
    self.active = True






