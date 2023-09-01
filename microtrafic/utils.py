import json
import random
import string
from typing import List
from dataclasses import dataclass


from matplotlib.colors import CSS4_COLORS

@dataclass
class Parameters:
    NVOIES: int
    ROAD_WIDTH: float
    ROAD_LEN: int
    VMAX: float
    VMIN: float
    NVOITURES: int
    DT: float
    TEMPS_SECUR: float
    sens_changement: dict

@dataclass
class Bornes:
    x: tuple
    y: tuple
    v: tuple


def read_params(file_name: str = 'parameters.json'):
    with open(file_name, "r") as json_file:
        return Parameters(**json.load(json_file))


def read_bornes(parameters: Parameters) -> Bornes:
    bornes_x = (-parameters.NVOIES + 1, 0)
    bornes_y = (0, parameters.ROAD_LEN - 1)
    bornes_v = (parameters.VMIN, 1)
    return Bornes(x=bornes_x, y=bornes_y, v=bornes_v)


def genere_impaires(n: int) -> List[int]:
    """ Pour 2 voies on veut [-1, -3] * road_width
             3 -> [-1, -3, -5]
             4 -> [-1, -3, -5, -7]
             ... Les nombres impais <= 2n - 1
    """
    return list(range(n+n))[1::2]


def generate_random_immatriculation() -> str:
    letters1 = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
    numbers = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
    letters2 = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)

    return letters1 + '-' + numbers + '-' + letters2


def generate_random_color() -> str:
    return random.choice(list(CSS4_COLORS.keys()))

