import curses
import time
from curses import wrapper

border = '|'
voiture = '▮'
road_w = 3

def main(stdscr):
    middle_w = curses.COLS // 2
    curses.curs_set(0)  # Masquer le curseur

    position = 0  # Position initiale de la voiture au milieu de l'écran

    # Afficher le titre
    title = "MICROTRAFIC"
    stdscr.addstr(0, middle_w - len(title)//2, title, curses.A_BOLD)
    # Afficher un message pour démarrer la simulation
    start = "Appuyer sur une touche pour commencer"
    stdscr.addstr(3, middle_w - len(start)//2, start, curses.A_ITALIC)
    stdscr.getkey()

    # Clear the screen once before starting the simulation
    stdscr.clear()
    stdscr.refresh()
    for i in range(0, curses.LINES):
        i %= curses.LINES
        stdscr.addstr(i, middle_w, border)
        stdscr.addstr(i, middle_w - road_w, border)
        stdscr.addstr(i, middle_w + road_w, border)

    # Ajout position initiale de la voiture
    voie1 = middle_w + road_w - road_w//2
    voie2 = middle_w - road_w + road_w//2
    position = [curses.LINES - 1, voie1]
    stdscr.addstr(position[0], position[1], voiture)
    # Boucle de simulation
    while True:
    
        #update_road(stdscr, position)
        # Attendre un court moment avant de rafraîchir l'écran pour simuler le mouvement
        time.sleep(0.5)

        # Effacer la position précédente de la voiture
        stdscr.addstr(position[0], position[1], ' ')
        # Mettre à jour la position de la voiture pour la faire bouger vers le bas
        position[0] -= 1
        stdscr.addstr(position[0] % curses.LINES, 0, str(position[0]))
        position[0] %= curses.LINES
        stdscr.addstr(position[0], position[1], voiture)
        stdscr.refresh()
        
wrapper(main)
