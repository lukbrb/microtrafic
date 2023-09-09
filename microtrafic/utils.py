import json
import random
import string
from typing import List
from dataclasses import dataclass
from matplotlib.colors import CSS4_COLORS
from microtrafic.core import Voiture

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


def check_distance(voiture: Voiture, l_voitures: List[Voiture], temps_secur: float) -> bool:
    distance_secur = voiture.v * temps_secur
    for other in l_voitures:
        for other in l_voitures:
            if voiture.x == other.x and voiture != other:  # Véhicules sur la même ligne, et pas lui-même
                if abs(voiture.y - other.y) < distance_secur:
                    return False
    return True

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


def generate_cars(nvoitures: int, bornes: Bornes, vmax: float, temps_secur: float, max_essais: int = 50) -> List[Voiture]:
    """ Généère une liste de voitures en s'assurant qu'elles 
        occupent toutes une position autorisée.
    """
    if not isinstance(bornes, Bornes):
        raise TypeError(f"bornes est de type {type(bornes)}, mais doit être de type Bornes.")
    
    # liste_basique = [Voiture(random.randint(*bornes.x), random.uniform(*bornes.y), random.uniform(*bornes.v) * vmax) for _ in range(nvoitures)]
    liste_voitures = []

    for i in range(nvoitures):
        can_be_added = False
        essai = 0
        while can_be_added is False and essai <= max_essais:
            voiture = Voiture(random.randint(*bornes.x), random.uniform(*bornes.y), random.uniform(*bornes.v) * vmax)
            can_be_added = check_distance(voiture, liste_voitures)  # if check_dist is True -> can_be_addded true, else can_be_added false
            essai += 1
        if can_be_added:    
            liste_voitures.append(voiture)
        else:
            print(f"{voiture.nom} n'a pas pu être placée. Nombre max de voiture")
        
    return liste_voitures


    # Il faut maintenant s'assurer que toutes les distances de sécurité soient respectées pour toutes les voitures, et sinon, changer la voiture à un autre endroit valide.
    # A priori, les insérer une par une pour procéder à une vérif semble le plus simple. 