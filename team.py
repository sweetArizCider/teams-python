
class Team:
  def __init__(self, name: str, sport: str, active: bool = True):
    self.name = name
    self.sport = sport
    self.active = active

  def __str__(self):
    return f"{self.name}, {self.sport}, active={self.active})"

  def change_name(self, new_name: str):
    if not new_name:
      return
    old_team_name = self.name
    self.name = new_name
    return

  def change_sport(self, new_sport: str):
    if not new_sport:
      return
    self.sport = new_sport

  def desactive(self):
    self.active = False

  def activate(self):
    self.active = True



if __name__ == '__main__':
  cruz_azul = Team('Cruz Azul', 'Baseball')
  cruz_azul.change_name('Cruz Azul FC')
  cruz_azul.change_sport('Soccer')
  cruz_azul.desactive()
  cruz_azul.activate()
  print(cruz_azul)

