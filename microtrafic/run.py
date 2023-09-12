from typing import List
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation

from datareader import read_params, read_bornes
from utils import genere_impaires
from core import initialise_voitures, Route

params = read_params()
bornes = read_bornes(params)

voitures = initialise_voitures(params.NVOITURES, bornes, params.VMAX, params.TEMPS_SECUR)
# voitures = initialise_voitures(params.NVOITURES, bornes, params.VMAX, params.TEMPS_SECUR, genre='facile')
route = Route(voitures, nvoies=params.NVOIES, distance=100)

fig, ax = plt.subplots()
ax.set_xlim(-params.NVOIES, 2 * params.ROAD_WIDTH)
ax.set_ylim(0, route.distance)
# ax.set_axis_off()

# ax.axis('off')
# Initialisation des points
points = [(ax.plot(voiture.x, voiture.y, color=voiture.couleur, marker='.', markersize=10))[0] for voiture in voitures]


# etape = [ax.plot(0, 0, '.k', label=f'Étape = {route.pas}')[0]]
# Création de la route 


def genere_route(axe: plt.Axes, road: Route, nvoies: int, rwidth: float) -> List[LineCollection]:
    multiplicateurs = genere_impaires(nvoies)
    ligne_droite = [axe.vlines(rwidth, 0, road.distance, color='w', linestyles='-')]
    interlignes = [axe.vlines(-i * params.ROAD_WIDTH, 0, road.distance, color='w', linestyles='--') for i in
                   multiplicateurs[:-1]]  # La dernière ligne doit être solide
    ligne_gauche = [axe.vlines(-multiplicateurs[-1] * params.ROAD_WIDTH, 0, road.distance, color='w', linestyles='-')]
    return ligne_droite + interlignes + ligne_gauche


ax.set_facecolor('gray')
lignes = genere_route(axe=ax, road=route, nvoies=params.NVOIES, rwidth=params.ROAD_WIDTH)


def update(frame):
    # Mettre à jour les coordonnées des points (simulation du mouvement)
    route.pas += 1
    route.step()

    for i in range(len(points)):
        # Mettre à jour les données des points dans les graphiques
        points[i].set_data(voitures[i].x, voitures[i].y % route.distance)
        # points[i].set_label(f'{voitures[i].nom} (y = {voitures[i].y: .2f})')
    # etape[0].set_label(f'Étape = {route.pas}')
    return points


# Durée totale de la simulation en secondes
total_duration = 3
# Taux de rafraîchissement (images par seconde)
fps = 30
total_frames = int(total_duration * fps)
# Créer l'animation en appelant la fonction update à chaque image (frame)
ani = FuncAnimation(fig, update, frames=total_frames, interval=1000 / fps, blit=True)
# ax.legend()

plt.tight_layout()  # Ajuster la disposition des éléments de la figure
plt.show()
# # ani.save('trafic.gif')
