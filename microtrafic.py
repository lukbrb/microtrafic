import itertools
import logging
from typing import List


dt = 0.1
NVOIES = 3
sens_changement = {'gauche': -1, 'droite': 1, 'devant': 1, 'derriere': -1}

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
    def __init__(self, x, y, v, nom="baniol", a=0) -> None:
        self.x = x
        self.y = y
        self.v = v
        self.a = a
        self.nom = nom

    def __str__(self) -> str:
        return f"{self.nom.title()}(x={self.x:.2f}, y={self.y:.2f}, v={self.v:.2f})"
    
    def __repr__(self) -> str:
        return f"{self.nom.title()}(x={self.x:.2f}, y={self.y:.2f}, v={self.v:.2f})"
    def avance(self) -> None:
        dy = 0.5 * self.a * dt**2 + self.v * dt
        self.y += dy
    
    def accelere(self, signe=1) -> None:
        dv += (self.a * dt) * signe # 1 accélère, -1 décélère
        self.v += dv
    
    def _change_voie(self, sens:str):
        dx = sens_changement[sens]
        if -NVOIES <= (self.x + dx) <= 0:
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

    def distance_securite(self, x: float, y: float, voiture: Voiture, temps_secur: float = 1.) -> bool:
        distance_secur = voiture.v * temps_secur
        for other in self.voitures:
            if x == other.x and voiture != other:  # Véhicules sur la même ligne, et pas lui-même
                if abs(y - other.y) < distance_secur:
                    return False
        return True
    
    def step(self) -> None:
        for voiture in self.voitures:
            if self.distance_securite(voiture.x + sens_changement['droite'], voiture.y + voiture.v * dt, voiture) and voiture.x < 0:
                voiture.rabattement()
                action = 'Rabattement'
            elif self.distance_securite(voiture.x, voiture.y + voiture.v * dt, voiture):
                voiture.avance()
                action = 'Avance'
            elif self.distance_securite(voiture.x + sens_changement['gauche'], voiture.y + voiture.v * dt, voiture) and (voiture.x - 1) > -NVOIES:
                voiture.depassement()
                action = 'Dépassement'
            else:
                voiture.attente()
                action = 'Attente'

            voiture.y %= self.distance
            logging.info(f"{voiture.nom.upper()} - Position ({voiture.x:.2f}, {voiture.y:.2f}) - Action: {action}")
            