#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.optimize import brentq
import timeit 
import numpy as np 
import matplotlib.pylab as plt 
import matplotlib.patches as mpatches
import os

from busqueda import bisec, punto_fijo, newton_raphson
from funciones import funcion_fuerza, derivada_fuerza

# Error y maxima cantidad de iteraciones
a_tol = 0.5e-15
n_max = 200

# Ignorar las warnings de division por cero
np.seterr(divide='ignore')


def generar_info_raices(mod_masa, int_bisec, int_punto, int_newton):
    ''' La siguiente funcion genera:
    El grafico de la fuerza segun el modificador de masa (m * g * mod_masa).
    La tabla de los tres metodos a partir de los intervalos especificados.
    Tres graficos de las diferencias absolutas de cada metodo, y un grafico general combinando los tres.
    '''

    # Generar grafico de la fuerza en funcion de y, con el modificador de masa especificado
    xx = np.linspace(-5, 5, 256+1)
    yy = funcion_fuerza(mod_masa)(xx)
    nombre = 'fuerza_m_' + str(mod_masa)
    plt.figure(figsize=(10,7))
    plt.plot(xx, yy, lw=2)
    plt.xlabel('x')
    plt.ylabel(nombre +'(x)')
    plt.title('Funcion '+ nombre)
    plt.grid(True)
    plt.savefig(nombre + '.png')


    # Biseccion
    l_izq = int_bisec[0]
    l_der = int_bisec[1]
    r, delta, n_iter_bisec, delta_abs_graph_bisec = bisec(funcion_fuerza(mod_masa), l_izq, l_der, a_tol, n_max, open('fuerza_m_' + str(mod_masa) + '_bisec.txt', 'w'))

    plt.figure(figsize=(10,7))
    plt.plot(range(n_iter_bisec), delta_abs_graph_bisec, 'b^', label='Biseccion')
    plt.grid(True)
    plt.yscale('log')
    plt.xlabel('i')
    plt.ylabel('|xi+1 - xi|')
    plt.legend(loc='upper right')
    plt.savefig('fuerza_m_' + str(mod_masa) + '_diff_bisec.png')


    # Punto fijo
    l_izq = int_punto[0]
    l_der = int_punto[1]
    r, delta, n_iter_punto, delta_abs_graph_punto = punto_fijo(funcion_fuerza(mod_masa), l_izq+(l_der-l_izq)/2, a_tol, n_max, open('fuerza_m_' + str(mod_masa) + '_punto.txt', 'w'))

    plt.figure(figsize=(10,7))
    plt.plot(range(n_iter_punto), delta_abs_graph_punto, 'ro', label='Punto fijo')
    plt.grid(True)
    plt.yscale('log')
    plt.xlabel('i')
    plt.ylabel('|xi+1 - xi|')
    plt.legend(loc='upper right')
    plt.savefig('fuerza_m_' + str(mod_masa) + '_diff_punto.png')


    # Newton-Raphson
    l_izq = int_newton[0]
    l_der = int_newton[1]
    r, delta, n_iter_newton, delta_abs_graph_newton = newton_raphson(funcion_fuerza(mod_masa), derivada_fuerza(), l_izq+(l_der-l_izq)/2, a_tol, n_max, open('fuerza_m_' + str(mod_masa) + '_newton.txt', 'w'))

    plt.figure(figsize=(10,7))
    plt.plot(range(n_iter_newton), delta_abs_graph_newton, 'gs', label='Newton-Raphson')
    plt.grid(True)
    plt.yscale('log')
    plt.xlabel('i')
    plt.ylabel('|xi+1 - xi|')
    plt.legend(loc='upper right')
    plt.savefig('fuerza_m_' + str(mod_masa) + '_diff_newton.png')


    # Grafico con los tres metodos
    plt.figure(figsize=(10,7))
    plt.plot(range(n_iter_newton), delta_abs_graph_newton, 'gs', label='Newton-Raphson')
    plt.plot(range(n_iter_punto), delta_abs_graph_punto, 'ro', label='Punto fijo')
    plt.plot(range(n_iter_bisec), delta_abs_graph_bisec, 'b^', label='Biseccion')
    plt.grid(True)
    plt.yscale('log')
    plt.xlabel('i')
    plt.ylabel('|xi+1 - xi|')
    plt.legend(loc='upper right')
    plt.savefig('fuerza_m_' + str(mod_masa) + '_diff.png')


print('Generando Ejercicio 1...')
os.makedirs('ej1', exist_ok=True)
os.chdir('ej1')
generar_info_raices(0, (-3.5, -1.5), (3.5, 1.5), (0, 1))
os.chdir('../')

print('Generando Ejercicio 2...')
os.makedirs('ej2', exist_ok=True)
os.chdir('ej2')
generar_info_raices(0.3, (-3.5, -1.5), (3.5, 1.5), (-1, 2))
os.chdir('../')

print('Generando Ejercicio 3...')
os.makedirs('ej3', exist_ok=True)
os.chdir('ej3')
generar_info_raices(0.3, (-1.5, 1), (-1, 1), (-.5, -.5))
os.chdir('../')

print('Generando Ejercicio 4...')
os.makedirs('ej4', exist_ok=True)
os.chdir('ej4')
file_ej4 = open('raices.txt', 'w')
print('{0:^4} {1:^17} {2:^17} {3:^17}'.format('m', 'Raiz 1', 'Raiz 2', 'Raiz 3'), file=file_ej4)
for i in range(2, 6):
    raices = []
    for j in range(-1, 2):
        r, _, _, _ = newton_raphson(funcion_fuerza(i * 0.3), derivada_fuerza(), 10.0 * j, a_tol, n_max, open(os.devnull, 'w'))
        raices.append(r)
    print('{0:.1f} {1: .14f} {2: .14f} {3: .14f}'.format(i * 0.3, *raices), file=file_ej4)
