import json
from dataclasses import dataclass


@dataclass
class Parameters:
    NVOIES: int
    road_width: float
    VMAX: int
    NVOITURES: int
    bornes_y: tuple
    bornes_v: tuple
    dt: float
    TEMPS_SECUR: float
    sens_changement: dict


def read_params(file_name):
    with open(file_name, "r") as json_file:
        return Parameters(**json.load(json_file))
        