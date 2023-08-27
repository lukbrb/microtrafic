import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from microtrafic import Voiture, Route, NVOIES


road_width = 0.5
VMAX = 5
NVOITURES = 40
bornes_x = (-NVOIES + 1, 0)
bornes_y = (0, 99)
bornes_v = (0.7, 1)

voitures = [Voiture(random.randint(*bornes_x), random.uniform(*bornes_y), random.uniform(*bornes_v) * VMAX) for _ in range(NVOITURES)]


# voitures = [Voiture(0, 1, v=VMAX, nom='Dacia'), 
#             Voiture(0, 15, v=0.8*VMAX, nom='Polo '), 
#             Voiture(0, 70, v=0.3*VMAX, nom='Camion 2'), 
#             Voiture(-1, 65, v=0.35*VMAX, nom='Camion 1'), 
#             Voiture(0, 40, v=0.6*VMAX, nom='4L   '),
#             Voiture(-1, 60, v=0.9*VMAX, nom='Cabrio')
#             ]
route = Route(voitures, nvoies=NVOIES, distance=100)

fig, ax = plt.subplots()
ax.set_xlim(-5, 5)
ax.set_ylim(0, route.distance)
#ax.set_axis_off()

#ax.axis('off')


couleurs = 'rbgkyw'
# Initialisation des points
points = [(ax.plot(voiture.x, voiture.y, color=voiture.couleur, marker='.', markersize=10))[0] for i, voiture in enumerate(voitures)]
etape = [ax.plot(0, 0, '.k', label=f'Étape = {route.pas}')[0]]
# Création de la route 

ax.set_facecolor('gray')
# TODO: Automatiser cette création en fonction de NVOIES
ligne1 = ax.vlines(road_width, 0, route.distance, color='w', linestyles='-')
ligne2 = ax.vlines(-road_width, 0, route.distance, color='w', linestyles='--')

ligne3 = ax.vlines(-3 * road_width, 0, route.distance, color='w', linestyles='--')
ligne4 = ax.vlines(-5 * road_width , 0, route.distance, color='w', linestyles='-')
# points = [point1, point2, point3]

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
