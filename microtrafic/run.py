import random
from typing import List
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation

from read_json import read_params, read_bornes
from microtrafic import Voiture, Route


# TODO: Mettre les paramètres généraux dans un fichier json ou autre
# road_width = 0.5
# VMAX = 5
# NVOITURES = 40
# bornes_x = (-NVOIES + 1, 0)
# bornes_y = (0, 99)
# bornes_v = (0.7, 1)
params = read_params()
bornes = read_bornes(params)

voitures = [Voiture(random.randint(*bornes.x), random.uniform(*bornes.y), random.uniform(*bornes.v) * params.VMAX) for _ in range(params.NVOITURES)]

route = Route(voitures, nvoies=params.NVOIES, distance=100)

fig, ax = plt.subplots()
ax.set_xlim(- params.NVOIES, 5)
ax.set_ylim(0, route.distance)
#ax.set_axis_off()

#ax.axis('off')


couleurs = 'rbgkyw'
# Initialisation des points
points = [(ax.plot(voiture.x, voiture.y, color=voiture.couleur, marker='.', markersize=10))[0] for i, voiture in enumerate(voitures)]
etape = [ax.plot(0, 0, '.k', label=f'Étape = {route.pas}')[0]]
# Création de la route 

def genere_impaires(n: int) -> List[int]:
    """ Pour 2 voies on veut [-1, -3] * road_width
             3 -> [-1, -3, -5]
             4 -> [-1, -3, -5, -7]
             ... Les nombres impais <= 2n - 1
    """
    return list(range(n+n))[1::2]

def genere_route(ax: plt.Axes, route: Route, nvoies: int, rwidth: float) -> List[LineCollection]:
    multiplicateurs = genere_impaires(nvoies)
    ligne_droite = [ax.vlines(rwidth, 0, route.distance, color='w', linestyles='-')]
    interlignes = [ax.vlines(-i * params.ROAD_WIDTH, 0, route.distance, color='w', linestyles='--') for i in multiplicateurs[:-1]]  # La dernière ligne doit être solide
    ligne_gauche = [ax.vlines(-multiplicateurs[-1] * params.ROAD_WIDTH, 0, route.distance, color='w', linestyles='-')]
    return ligne_droite + interlignes + ligne_gauche

ax.set_facecolor('gray')
lignes = genere_route(ax=ax, route=route, nvoies=params.NVOIES, rwidth=params.ROAD_WIDTH)

def update(frame):
    # Mettre à jour les coordonnées des points (simulation du mouvement)
    route.pas += 1
    route.step()

    for i in range(len(points)):
    # Mettre à jour les données des points dans les graphiques
        points[i].set_data(voitures[i].x, voitures[i].y % route.distance)
        points[i].set_label(f'{voitures[i].nom} (y = {voitures[i].y: .2f})')
    etape[0].set_label(f'Étape = {route.pas}')
    return points + etape

# Durée totale de la simulation en secondes
total_duration = 3
# Taux de rafraîchissement (images par seconde)
fps = 30
total_frames = int(total_duration * fps)
# Créer l'animation en appelant la fonction update à chaque image (frame)
ani = FuncAnimation(fig,update, frames=range(total_frames), interval=1000/fps, blit=True)
ax.legend()

plt.tight_layout()  # Ajuster la disposition des éléments de la figure
plt.show()
# ani.save('trafic.gif')
