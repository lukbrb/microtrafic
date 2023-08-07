import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

dt = 0.1
class Route:
    def __init__(self, voitures, nvoies, distance) -> None:
        self.voitures = voitures
        self.nvoies = nvoies
        self.distance = distance

    def evolve(self):
        for voit in self.voitures:
            for other in self.voitures:
                if voit != other:
                    if voit.check_distance_securite(other):
                        voit.avance()
                    else:
                        # print(f"{voit.nom} (x={voit.y}) trop proche de {other.nom} (x={other.y})")
                        # print(f"{voit.nom} passe de v={voit.v} à {other.v}...")
                        # voit.v = other.v
                        voit.change_voie(-1)

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

    def change_voie(self, dx):
        self.x += dx
    
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


if __name__ == '__main__':

    voitures = [Voiture(0, 3, v=5, nom='Dacia'), Voiture(0, 30, v=3, nom='Polo'), Voiture(0, 50, v=2, nom='4L')]
    route = Route(voitures, nvoies=1, distance=100)

    # roule = True
    # while roule:
    #     for voit in voitures:
    #         if voit.x > route.distance:
    #             roule = False
        
    #     route.evolve()

    # for voit in voitures:
    #     print(voit.nom, voit.x, voit.v)


    # Création de la figure et de l'axe
    fig, ax = plt.subplots()
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, route.distance)

    # Initialisation des points
    point1, = ax.plot(voitures[0].x, voitures[0].y, 'r.', markersize=10, label=voitures[0].nom)
    point2, = ax.plot(voitures[1].x, voitures[1].y, 'b.', markersize=10, label=voitures[1].nom)
    point3, = ax.plot(voitures[2].x, voitures[2].y, 'g.', markersize=10, label=voitures[2].nom)
    ligne1 = ax.vlines(-0.3, 0, route.distance, color='k')
    ligne2 = ax.vlines(0.3, 0, route.distance, color='k')
    ligne3 = ax.vlines(0.9, 0, route.distance, color='k')
    ligne4 = ax.vlines(-0.9, 0, route.distance, color='k')
    points = [point1, point2, point3]

    def update(frame):
        # Mettre à jour les coordonnées des points (simulation du mouvement)
        route.evolve()

        for i in range(3):
        # Mettre à jour les données des points dans les graphiques
            points[i].set_data(voitures[i].x, voitures[i].y % route.distance)

        # Renvoie une liste des graphiques qui ont été mis à jour
        return points

    # Durée totale de la simulation en secondes
    total_duration = 3
    # Taux de rafraîchissement (images par seconde)
    fps = 30
    total_frames = int(total_duration * fps)
    # Créer l'animation en appelant la fonction update à chaque image (frame)
    ani = FuncAnimation(fig,update, frames=range(total_frames), interval=1000/fps, blit=True)
    plt.legend()
    # plt.show()
    ani.save('trafic.gif')
