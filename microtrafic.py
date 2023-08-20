import itertools
from typing import List
import numpy as np


dt = 0.1
NVOIES = 3
VMAX = 5
sens_changement = {'gauche': 1, 'droite': -1, 'devant': 1, 'derriere': -1}

""""
Conditions pour avancer:
- Distance de sécurité avant suffisante

Conditions pour dépasser:
- Distance de sécurité avant trop faible
- Distance de sécurité arrière 

Note: Bogue lorsqu'une voiture revient à 0, car dans ce cas les distances de sécurité sont faussement respectées.
"""

class Voiture:
    def __init__(self, x, y, v, nom, a=0) -> None:
        self.x = x
        self.y = y
        self.v = v
        self.a = a
        self.nom = nom
    
    def avance(self):
        dy = 0.5 * self.a * dt**2 + self.v * dt
        self.y += dy
    
    def accelere(self, signe=1):
        dv += (self.a * dt) * signe # 1 accélère, -1 décélère
        self.v += dv

    def check_distance_securite(self, other, sens: str):
        "True si distance respectée, False sinon"
        temps_secur = 2 # en secondes
        distance_secur = self.v * temps_secur
        dy = sens_changement[sens]
        dist_voit = (other.y - self.y) * dy
        
        # Voiture derrière, devant : d < 0, d > 0
        # Direction derrière, devant: dy < 0, dy > 0
        # d < 0 et dy < 0 --> dist_voit > 0 ---> SI  dist_voit > distance_secur : OK
        # d < 0 et dy > 0 --> dist_voit < 0 ---> OK
        # d > 0 et dy < 0 --> dist_voit < 0 ---> OK
        # d > 0 et dy > 0 --> dist_voit > 0 ---> SI  dist_voit > distance_secur : OK

        if other.x != self.x:
            return True

        if dist_voit < 0: 
            return True

        if dist_voit > distance_secur:
            return True
        else:
            return False
        
        # return !((other.y - self.y) <= distance_secur)

    def can_depasse(self, other, sens: str, nvoie: int):
        dx = sens_changement[sens]

        can_overtake = False
        x_temp = self.x
        self.x += dx
        if self.check_distance_securite(other, sens='devant') and self.check_distance_securite(other, sens='derriere') and self.x >= nvoie:
            can_overtake = True
        self.x = x_temp
        return can_overtake
    
    def change_voie(self, sens:str, nvoie:int):
        dx = sens_changement[sens]
        dy = 0  # Un p'tit coup d'accélérateur
        if self.x >= nvoie:
            self.x += dx
            self.y += dy
    
    def depassement(self):
         self.change_voie(sens='gauche', nvoie=-NVOIES)
    
    def rabattement(self):
        self.change_voie(sens='droite', nvoie=-NVOIES)

class Route:
    def __init__(self, voitures: List[Voiture], nvoies, distance) -> None:
        self.voitures = voitures
        self.nvoies = nvoies - 1
        self.distance = distance
        self.nvoitures = len(self.voitures)

    def evolve(self):
        for voit in self.voitures:  #  for i, j in itertools.combinations(range(self.N_ATOMS), 2):
            for other in self.voitures:
                if voit != other:
        # for voit, other in itertools.combinations(self.voitures, 2):
                    if voit.check_distance_securite(other, sens='devant'):
                        voit.avance()
                    elif voit.can_depasse(other, sens='droite', nvoie=-self.nvoies):
                        voit.rabattement()
                    else:
                        voit.x = voit.x  # on attends
                                            
                    if voit.x < 0 and voit.can_depasse(other, sens='gauche', nvoie=-self.nvoies):
                        voit.depassement()


            voit.y %= self.distance
