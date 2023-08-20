import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from microtrafic import Voiture, Route, NVOIES, VMAX

road_width = 0.5


voitures = [Voiture(0, 3, v=VMAX, nom='Dacia'), Voiture(0, 3, v=0.9*VMAX, nom='Polo'), Voiture(0, 50, v=0.7*VMAX, nom='4L')]
route = Route(voitures, nvoies=NVOIES, distance=100)

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

    for i in range(len(points)):
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
