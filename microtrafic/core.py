import logging
import random
from typing import List

from datareader import read_params, Bornes
from utils import generate_random_color, generate_random_immatriculation

params = read_params()

""""
Conditions pour avancer:
- Distance de sécurité avant suffisante

Conditions pour dépasser:
- Distance de sécurité avant trop faible
- Distance de sécurité arrière suffisante

Note: Bogue lorsqu'une voiture revient à 0, car dans ce cas les distances de sécurité sont faussement respectées.
"""

logging.basicConfig(level=logging.INFO, format='%(message)s')

log_file = "run.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(file_formatter)

logging.getLogger('').addHandler(file_handler)


class Voiture:
    def __init__(self, x, y, v, nom=None, couleur=None, a=0) -> None:
        self.x = x
        self.y = y
        self.v = v
        self.a = a
        self.nom = nom
        self.couleur = couleur
        self.set_color()
        self.set_name()

    def __str__(self) -> str:
        return f"{self.nom}(x={self.x:.2f}, y={self.y:.2f}, v={self.v:.2f})"

    def __repr__(self) -> str:
        return f"{self.nom}(x={self.x:.2f}, y={self.y:.2f}, v={self.v:.2f})"

    def set_color(self) -> None:
        self.couleur = generate_random_color() if self.couleur is None else self.couleur

    def set_name(self) -> None:
        self.nom = generate_random_immatriculation() if self.nom is None else self.nom

    def avance(self) -> None:
        dy = 0.5 * self.a * params.DT ** 2 + self.v * params.DT
        self.y += dy

    def accelere(self, signe=1) -> None:
        dv = (self.a * params.DT) * signe  # 1 accélère, -1 décélère
        self.v += dv

    def _change_voie(self, sens: str):
        dx = params.sens_changement[sens]
        if -params.NVOIES <= (self.x + dx) <= 0:
            self.x += dx

    def depassement(self):
        self._change_voie(sens='gauche')
        self.avance()

    def rabattement(self):
        self._change_voie(sens='droite')
        self.avance()

    def attente(self) -> None:
        self.y = self.y


class Route:
    def __init__(self, voitures: List[Voiture], nvoies: int, distance: float) -> None:
        self.voitures = voitures
        self.nvoies = nvoies - 1
        self.distance = distance
        self.nvoitures = len(self.voitures)
        self.pas = 0

    def distance_securite(self, x: float, y: float, voiture: Voiture, temps_secur: float = 1.) -> bool:
        distance_secur = voiture.v * temps_secur
        for other in self.voitures:
            if x == other.x and voiture != other:  # Véhicules sur la même ligne, et pas lui-même
                if abs(y % self.distance - other.y % self.distance) < distance_secur:
                    return False
        return True

    def step(self) -> None:
        for voiture in self.voitures:
            if self.distance_securite(voiture.x + params.sens_changement['droite'], voiture.y + voiture.v * params.DT,
                                      voiture) and voiture.x < 0:
                voiture.rabattement()
                action = "S'est rabattu"
            elif self.distance_securite(voiture.x, voiture.y + voiture.v * params.DT, voiture):
                voiture.avance()
                action = 'A avancé'

            elif self.distance_securite(voiture.x + params.sens_changement['gauche'], voiture.y + voiture.v * params.DT,
                                        voiture) and (voiture.x - 1) > -params.NVOIES:
                voiture.depassement()
                action = 'A dépassé'
            else:
                voiture.attente()
                action = 'A attendu'

            voiture.y %= self.distance
            logging.info(
                f"Étape : {self.pas} - {voiture.nom}- Position ({voiture.x:.2f}, {voiture.y:.2f}) - Action: {action}")

def check_distance(voiture: Voiture, l_voitures: List[Voiture], temps_secur: float) -> bool:
    distance_secur = voiture.v * temps_secur
    for other in l_voitures:
        for other in l_voitures:
            if voiture.x == other.x and voiture != other:  # Véhicules sur la même ligne, et pas lui-même
                if abs(voiture.y - other.y) < distance_secur:
                    return False
    return True


def initialise_voitures(nvoitures: int, bornes: Bornes, vmax: float, temps_secur: float, max_essais: int = 50, genre='normal') -> List[Voiture]:
    """ Généère une liste de voitures en s'assurant qu'elles 
        occupent toutes une position autorisée.
    """
    if not isinstance(bornes, Bornes):
        raise TypeError(f"bornes est de type {type(bornes)}, mais doit être de type Bornes.")
    
    if genre == 'normal':
        # liste_basique = [Voiture(random.randint(*bornes.x), random.uniform(*bornes.y), random.uniform(*bornes.v) * vmax) for _ in range(nvoitures)]
        liste_voitures = []

        for i in range(nvoitures):
            can_be_added = False
            essai = 0
            while can_be_added is False and essai <= max_essais:
                voiture = Voiture(random.randint(*bornes.x), random.uniform(*bornes.y), random.uniform(*bornes.v) * vmax)
                can_be_added = check_distance(voiture, liste_voitures, temps_secur)  # if check_dist is True -> can_be_addded true, else can_be_added false
                essai += 1
            if can_be_added:    
                liste_voitures.append(voiture)
            else:
                print(f"{voiture.nom} n'a pas pu être placée. Nombre max de voiture")
            
        return liste_voitures
    elif genre == 'facile':
        return [Voiture(random.randint(*bornes.x), random.uniform(*bornes.y), random.uniform(*bornes.v) * vmax) for _ in range(nvoitures)]
    
    else:
        raise ValueError(f'Genre doit être normal ou facile, pas {genre}')