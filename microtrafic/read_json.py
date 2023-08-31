import json
from dataclasses import dataclass


@dataclass
class Parameters:
    NVOIES: int
    ROAD_WIDTH: float
    VMAX: int
    NVOITURES: int
    DT: float
    TEMPS_SECUR: float
    bornes_y: tuple
    bornes_v: tuple
    sens_changement: dict


def read_params(file_name):
    with open(file_name, "r") as json_file:
        return Parameters(**json.load(json_file))
        