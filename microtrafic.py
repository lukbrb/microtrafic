import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

dt = 0.1
NVOIES = 3
class Route:
    def __init__(self, voitures, nvoies, distance) -> None:
        self.voitures = voitures
        self.nvoies = nvoies - 1
        self.distance = distance
        self.nvoitures = len(self.voitures)

    def evolve(self):
        for voit in self.voitures:  #  for i, j in itertools.combinations(range(self.N_ATOMS), 2):
            for other in self.voitures:
                if voit != other:
        # for voit, other in itertools.combinations(self.voitures, 2):
                    if voit.check_distance_securite(other):
                        voit.avance()
                    elif voit.can_depasse(other, -1, -self.nvoies):
                        voit.change_voie(-1, -self.nvoies)
                    else:
                        voit.x = voit.x  # on attends
                                            
                    if voit.x < 0 and voit.can_depasse(other, 1, -self.nvoies):
                        voit.change_voie(1, -self.nvoies)


            voit.y %= self.distance

""""
Conditions pour avancer:
- Distance de sécurité avant suffisante

Conditions pour dépasser:
- Distance de sécurité avant trop faible
- Distanec de sécurité arrière 

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

    def change_voie(self, dx, nvoie):
        dy = 0  # Un p'tit coup d'accélérateur
        if self.x >= nvoie:
            self.x += dx
            self.y += dy
    
    
    def check_distance_securite(self, other):
        "True si distance respectée, False sinon"
        temps_secur = 2 # en secondes
        distance_secur = self.v * temps_secur
        if other.x != self.x:
            return True
        if (other.y - self.y) < 0:  # L'autre voiture est derrière
            return True

        if (other.y - self.y) < distance_secur:
            return False
        else:
            return True
        
        # return !((other.y - self.y) <= distance_secur)

    def can_depasse(self, other, dx, nvoie):
        can_overtake = False
        x_temp = self.x
        self.x += dx
        if self.check_distance_securite(other) and self.x >= nvoie:
            can_overtake = True
        self.x = x_temp
        return can_overtake


if __name__ == '__main__':

    voitures = [Voiture(0, 3, v=3, nom='Dacia'), Voiture(0, 30, v=2, nom='Polo'), Voiture(0, 50, v=1.5, nom='4L')]
    route = Route(voitures, nvoies=NVOIES, distance=100)

    # roule = True
    # while roule:
    #     for voit in voitures:
    #         if voit.x > route.distance:
    #             roule = False
        
    #     route.evolve()

    # for voit in voitures:
    #     print(voit.nom, voit.x, voit.v)

    road_width = 0.5
    # Création de la figure et de l'axe
    fig, ax = plt.subplots()
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, route.distance)
    couleurs = 'rbg'
    # Initialisation des points
    points = [(ax.plot(voiture.x, voiture.y, couleurs[i] + '.', markersize=10, label=voiture.nom))[0] for i, voiture in enumerate(voitures)]
    # Création de la route 
    # TODO: Automatiser cette création en fonction de NVOIES
    ligne1 = ax.vlines(road_width, 0, route.distance, color='k')
    ligne2 = ax.vlines(-road_width, 0, route.distance, color='k')
    ligne3 = ax.vlines(-3 * road_width, 0, route.distance, color='k')
    ligne4 = ax.vlines(-5 * road_width , 0, route.distance, color='k')
    # points = [point1, point2, point3]
    
    def update(frame):
        # Mettre à jour les coordonnées des points (simulation du mouvement)
        route.evolve()

        for i in range(3):
        # Mettre à jour les données des points dans les graphiques
            points[i].set_data(voitures[i].x, voitures[i].y % route.distance)
            points[i].set_label(f'{voitures[i].nom} (y = {voitures[i].y: .2f})')
            
            # print(f'{voitures[i].nom} , y = {voitures[i].x: .2f})')
        # Renvoie une liste des graphiques qui ont été mis à jour
        return points

    # Durée totale de la simulation en secondes
    total_duration = 3
    # Taux de rafraîchissement (images par seconde)
    fps = 30
    total_frames = int(total_duration * fps)
    # Créer l'animation en appelant la fonction update à chaque image (frame)
    ani = FuncAnimation(fig,update, frames=range(total_frames), interval=1000/fps, blit=True)
    ax.legend()
    plt.show()
    # ani.save('trafic.gif')
