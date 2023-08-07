import time
import numpy as np
import os


def print_matrix(mat):
    route = ''
    for i in range(0, len(mat)):
        for j in range(0, len(mat[0])):
            route += mat[i][j]
        route += '\n'
    print(route)

# def construct_matrix():
#     route = [['|', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|',  ' ', ' ', ' ', '|'], 
#              ['|', ' ', ' ', ' ', '|'],
#              ['|', ' ', ' ', ' ', '|'],
#              ['|', ' ', ' ', ' ', '|']
#              ]
#     voiture = '▮'
#     route[0][2] = voiture
#     return route

def construct_matrix(n_voies, road_len=10, road_width=3):
    route = [list((n_voies * ('|' + ' ' * road_width) + '|')) for _ in range(road_len)]
    return route

def find_indices(x, y, road_width):
    if y == 1:
        return road_width//2 + 1 
    else:
        return find_indices(x, y-1, road_width) + road_width + 1

def place_gova(x, y, mat, road_width=3, voiture = '▮'):
    y = find_indices(x, y, road_width)
    mat[x][y] = voiture
    return mat


# for i in range(5):
#     xrand = int(np.random.randint(0, 9, 1))
#     yrand = int(np.random.randint(1, 5, 1))
#     print(xrand, yrand)
#     route = place_gova(xrand, yrand, route, road_width=3)
#     print_matrix(route)
#     time.sleep(1)

"""
y, char
1 | 3
2 | 7
3 | 11
4 | 15
"""

class gova:
    def __init__(self, x= 1, y = 2):
        self.x = x
        self.y = y

    def move(self):
        self.x -= 1


route = construct_matrix(3, road_len=100)
voit = gova(x=8, y=1)
print_matrix(route)
i = 0
while i < 95:    
    route = place_gova(voit.x, voit.y, route)
    voit.move()
    route = construct_matrix(3, road_len=100)
    route= place_gova(voit.x, voit.y, route)
    print_matrix(route)
    if i == 2:
        voit.y +=1
    if i == 6:
        voit.y += 1
    i+=1
    time.sleep(1)
    os.system('clear')
    