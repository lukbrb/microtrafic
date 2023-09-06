import logging
from typing import List

from utils import read_params, generate_random_color, generate_random_immatriculation

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
                if abs(y - other.y % self.distance) < distance_secur:
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
