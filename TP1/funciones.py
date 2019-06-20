import numpy as np

#Constantes
NP = 101109  # Padron Camila Dvorkin
L0 = 1.98 # 2*100000 / NP #m
k = 10 #N/m
m0 = 0.989 # 100000/NP #kg
a = 1 #m
g = 9.81 #m/s**2


def funcion_fuerza(mod_masa):
	return lambda y: (-2*k*y * (1 - L0 / np.sqrt(y**2 + a**2)) - m0 * g * mod_masa) / (-2*k)


def derivada_fuerza():
	return lambda y: ((-2 *k *L0 * y**2)/(np.sqrt((a**2 + y**2)**3)) - 2 * k *(1 - L0/(np.sqrt(a**2 + y**2)))) / (-2*k)
