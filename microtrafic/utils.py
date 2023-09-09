import random
import string
from typing import List
from matplotlib.colors import CSS4_COLORS

def genere_impaires(n: int) -> List[int]:
    """ Pour 2 voies on veut [-1, -3] * road_width
             3 -> [-1, -3, -5]
             4 -> [-1, -3, -5, -7]
             ... Les nombres impais <= 2n - 1
    """
    return list(range(n+n))[1::2]


def generate_random_immatriculation() -> str:
    letters1 = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
    numbers = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
    letters2 = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)

    return letters1 + '-' + numbers + '-' + letters2


def generate_random_color() -> str:
    return random.choice(list(CSS4_COLORS.keys()))


    # Il faut maintenant s'assurer que toutes les distances de sécurité soient respectées pour toutes les voitures, et sinon, changer la voiture à un autre endroit valide.
    # A priori, les insérer une par une pour procéder à une vérif semble le plus simple. 