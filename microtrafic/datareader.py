import json
from typing import List
from dataclasses import dataclass

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
