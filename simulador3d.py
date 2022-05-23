import matplotlib.pyplot as plt
import numpy as np
from math import *

cubeMatrix = np.matrix([[1,7, 7, 1, 4], [1, 1, 1, 1, 7], [1, 1, 7, 7, 4], [1, 1, 1, 1, 1]])
points = [["0", "1", "0"], ["1", "0", "0"], ["0", "0", "0"]]
pov = ["40", "10", "80"]
pov = input("Primeiro ponto de vista: ").split(",")

#Função que calcula o vetor normal ao plano de projeção
#Usamos a fórmula que está na especificação do trabalho:
#𝑛x = 𝑦1𝑦2 . 𝑧3𝑧2 − 𝑦3. 𝑦2 . 𝑧1𝑧2
#𝑛y = −(𝑥1𝑥2 . 𝑧3𝑧2 − 𝑥3𝑥2 . 𝑧1. 𝑧2)
#𝑛z = 𝑥1𝑥3. 𝑦3𝑦2 − 𝑥3𝑥2 . 𝑦1. 𝑦2
#Contudo, está fórmula não funcionou para planos são definidos por
#pontos que possuem coordenadas na origem. Tendo isto em vista, deixamos
#o plano de projeção definido como z = 0;
def calcN(points):
    p1 = points[0]
    p2 =  points[1]
    p3 = points[2]
    nx = (int(p1[1]) * int(p2[1])) *  (int(p3[2]) * int(p2[2])) - ((int(p3[1]) * int(p2[1])) * (int(p1[2]) * int(p2[2])))
    ny = -1 * (int(p1[0]) * int(p2[0])) *  (int(p3[2]) * int(p2[2])) - ((int(p3[0]) * int(p2[0])) * (int(p1[2]) * int(p2[2])))
    nz = (int(p1[0]) * int(p2[0])) *  (int(p3[1]) * int(p2[1])) - ((int(p3[0]) * int(p2[0])) * (int(p1[1]) * int(p2[1])))
    return nx, ny, nz

def calcD(pov, points):
    # nx, ny, nz = calcN(points)
    nx, ny, nz = 0, 0, 1
    a, b, c = int(pov[0]), int(pov[1]), int(pov[2])
    point = points[0]

    d0 = (int(point[0])*nx) + (int(point[1]) * ny) + (int(point[2]) * nz)
    d1 = (a * nx) + (b * ny) + (c * nz)
    d = d0 - d1

    return d, d0, d1

def buildMatrix(pov, points):
    # nx, ny, nz = calcN(points)
    nx, ny, nz = 0, 0, 1

    d, d0, d1 = calcD(pov, points)
    a, b, c = int(pov[0]), int(pov[1]), int(pov[2])
    return np.matrix([[d + a*nx, a*ny, a*nz, -1*a*d0], 
    [b*nx, d+b*ny, b*nz, -1*b*d0], 
    [c*nx, c*ny, d+c*nz, -1*c*d0],
    [nx, ny, nz, -d1]])

def finalMatrix(objectMatrix):
    w = objectMatrix[3].getA1()
    line1 = objectMatrix[0].getA1()
    line2 = objectMatrix[1].getA1()
    line3 = objectMatrix[2].getA1()
    return np.matrix([
        [line1[0]/w[0], line1[1]/w[1], line1[2]/w[2], line1[3]/w[3], line1[4]/w[4]],
        [line2[0]/w[0], line2[1]/w[1], line2[2]/w[2], line2[3]/w[3], line1[4]/w[4]],
        [line3[0]/w[0], line3[1]/w[1], line3[2]/w[2], line3[3]/w[3], line1[4]/w[4]]
    ])

def main():
    print(finalMatrix)
    arestas = [[0,1],[2,1],[2,3],[3,0],[0,4],[1,4],[2,4],[3,4]]
    for aresta in arestas:
        x, y = finalMatrix[0].getA1(), finalMatrix[1].getA1()
        plt.plot([x[aresta[0]], x[aresta[1]]], [y[aresta[0]], y[aresta[1]]], marker="o",color="blue")
    

    plt.plot(x, y, marker = "o", color = "blue")
    plt.grid()
    plt.show()

if __name__ == '__main__':
    objectMatrix = buildMatrix(pov, points) * cubeMatrix
    print(buildMatrix(pov, points))
    finalMatrix = finalMatrix(objectMatrix)
    main()