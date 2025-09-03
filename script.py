from team import Team
from player import Player
from player_team import PlayerTeam

def app():
    cruz_azul = Team('Cruz Azul', 'Soccer')
    print(f"Team's name -> {cruz_azul.name}, sport -> {cruz_azul.sport}, is active? -> {cruz_azul.active}")
    cruz_azul.change_name('Cruz Azul FC')
    cruz_azul.change_sport('Baseball')
    cruz_azul.desactive()
    cruz_azul.activate()
    print(f"Team's name -> {cruz_azul.name}, sport -> {cruz_azul.sport}, is active? -> {cruz_azul.active}")

    carlos = Player('Carlos Arizpe', 21)
    sofia = Player("Sofía Delgado", 19)
    marco = Player("Marco Ruiz", 22)
    ana = Player("Ana Fernández", 20)
    liam = Player("Liam Torres", 23)
    valeria = Player("Valeria Gómez", 18)
    diego = Player("Diego Navarro", 24)
    lucia = Player("Lucía Herrera", 21)
    mateo = Player("Mateo Castillo", 20)
    elena = Player("Elena Rivas", 22)
    bruno = Player("Bruno Morales", 19)

    players = [
        carlos,
        sofia,
        marco,
        ana,
        liam,
        valeria,
        diego,
        lucia,
        mateo,
        elena,
        bruno,
    ]

    players_team = PlayerTeam(cruz_azul, players)

    players_team.list_players()


if __name__ == '__main__':
    app()
