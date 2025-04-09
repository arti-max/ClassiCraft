from ursina import *
import random as rnd
# Game Classes
from src.Constants import *
from src.Level.World import World
from src.Player import Player



app = Ursina()

chunks = []
chunks_to_load = []

player = Player()
player.y = 10
player.x = 2
world = World(player)


def input(key):
    if key == 'right mouse down':
        world.destroy_block()
    elif key == 'r' or key == 'R':
        player.air_time = 0
        player.y = 10
        player.x = rnd.randint(1, 4)
        player.z = rnd.randint(1, 4)


# FIXME сделать экран загрузки асинхронный, чтобы оно не зависало на этапе генерации
def update():
    # Загружаем по 1 чанку за кадр
    # player.update()
    world.update()


app.run()