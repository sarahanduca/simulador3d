#%matplotlib inline
from typing import final
import pygame
import numpy as np
from math import *

# WHITE = (255, 255, 255)
# RED = (0, 0, 0)
# BLACK = (0, 255, 0)

# WIDTH, HEIGHT = 800, 600
# pygame.display.set_caption("3D projection in pygame!")
# screen = pygame.display.set_mode((WIDTH, HEIGHT))

# scale = 100

# circle_pos = [WIDTH/2, HEIGHT/2]  # x, y

# angle = 0

cubeMatrix = np.matrix([[1,7, 7, 1, 4], [1, 1, 1, 1, 7], [1, 1, 7, 7, 4], [1, 1, 1, 1, 1]])
points = [["3", "2", "1"], ["1", "2", "1"], ["2", "1", "3"]]
pov = ["4", "5", "7"]
# pov = input("Primeiro ponto de vista: ").split(",")
# for i in range(3):
#     points.append(input("Digite um ponto do plano: ").split(","))


def calcN(points):
    p1 = points[0]
    p2 =  points[1]
    p3 = points[2]
    nx = (int(p1[1]) * int(p2[1])) *  (int(p3[2]) * int(p2[2])) - ((int(p3[1]) * int(p2[1])) * (int(p1[2]) * int(p2[2])))
    ny = -1 * (int(p1[0]) * int(p2[0])) *  (int(p3[2]) * int(p2[2])) - ((int(p3[0]) * int(p2[0])) * (int(p1[2]) * int(p2[2])))
    nz = (int(p1[0]) * int(p2[0])) *  (int(p3[1]) * int(p2[1])) - ((int(p3[0]) * int(p2[0])) * (int(p1[1]) * int(p2[1])))

    return nx, ny, nz

def calcD(pov, points):
    nx, ny, nz = calcN(points)
    a, b, c = int(pov[0]), int(pov[1]), int(pov[2])
    point = points[0]

    d0 = (int(point[0])*nx) + (int(point[1]) * ny) + (int(point[2]) * nz)
    d1 = (a * nx) + (b * ny) + (c * nz)

    return d0 - d1, d0

def buildMatrix(pov, points):
    nx, ny, nz = calcN(points)
    d, d0 = calcD(pov, points)
    a, b, c = int(pov[0]), int(pov[1]), int(pov[2])
    return np.matrix([[d + a*nx, a*ny, a*nz, -1*a*d0], 
    [b*nx, d+b*ny, b*nz, -1*b*d0], 
    [c*nx, c*ny, d+c*nz, -1*c*d0],
    [nx, ny, nz, 1]])

def finalMatrix(objectMatrix):
    w = objectMatrix[3].getA1()
    line1 = objectMatrix[0].getA1()
    line2 = objectMatrix[1].getA1()
    line3 = objectMatrix[2].getA1()
    finalMatrix = np.matrix([
        [line1[0]/w[0], line1[1]/w[1], line1[2]/w[2], line1[3]/w[3]],
        [line2[0]/w[0], line2[1]/w[1], line2[2]/w[2], line2[3]/w[3]],
        [line3[0]/w[0], line3[1]/w[1], line3[2]/w[2], line3[3]/w[3]]
    ])
    return finalMatrix.getT()
    
objectMatrix = buildMatrix(pov, points) * cubeMatrix
finalMatrix = finalMatrix(objectMatrix)

# all the cube vertices
displayVertex = []
displayVertex.append(np.matrix(finalMatrix[0].getA1()))
displayVertex.append(np.matrix(finalMatrix[1].getA1()))
displayVertex.append(np.matrix(finalMatrix[2].getA1()))
displayVertex.append(np.matrix(finalMatrix[3].getA1()))

# print(points)

# projection_matrix = np.matrix([
#     [1, 0, 0],
#     [0, 1, 0]
# ])


# projected_points = [
#     [n, n] for n in range(len(points))
# ]


# def connect_points(i, j, points):
#     pygame.draw.line(
#         screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


# clock = pygame.time.Clock()
# while True:

#     clock.tick(60)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 pygame.quit()
#                 exit()

#     # update stuff

#     rotation_z = np.matrix([
#         [cos(angle), -sin(angle), 0],
#         [sin(angle), cos(angle), 0],
#         [0, 0, 1],
#     ])

#     rotation_y = np.matrix([
#         [cos(angle), 0, sin(angle)],
#         [0, 1, 0],
#         [-sin(angle), 0, cos(angle)],
#     ])

#     rotation_x = np.matrix([
#         [1, 0, 0],
#         [0, cos(angle), -sin(angle)],
#         [0, sin(angle), cos(angle)],
#     ])
#     angle += 0.01

#     screen.fill(WHITE)
#     # drawining stuff

#     i = 0
#     for point in points:
#         rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
#         rotated2d = np.dot(rotation_y, rotated2d)
#         rotated2d = np.dot(rotation_x, rotated2d)

#         projected2d = np.dot(projection_matrix, rotated2d)

#         x = int(projected2d[0][0] * scale) + circle_pos[0]
#         y = int(projected2d[1][0] * scale) + circle_pos[1]

#         projected_points[i] = [x, y]
#         pygame.draw.circle(screen, RED, (x, y), 5)
#         i += 1

#     for p in range(4):
#         connect_points(p, (p+1) % 4, projected_points)
#         connect_points(p+4, ((p+1) % 4) + 4, projected_points)
#         connect_points(p, (p+4), projected_points)

#     pygame.display.update()