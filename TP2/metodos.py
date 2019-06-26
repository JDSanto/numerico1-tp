import numpy as np
import sys
from funciones import temperatura_exacta

def temps_a_celsius(arr):
	for x in range(len(arr)):
		arr[x] = arr[x] - 273 		# Kelvin a Celsius


def tiempos_a_minutos(arr):
	for x in range(len(arr)):
		arr[x] = arr[x] / 60		# Segundos a minutos


def euler(f, t0, t_fin, y0, h):
	resultados_y = []
	resultados_t = []

	w = y0
	t = t0

	resultados_y.append(w)
	resultados_t.append(t)

	i = 1
	while t <= t_fin:
		w = w + h * f(t, w)
		t = t0 + i * h
		resultados_y.append(w)
		resultados_t.append(t)
		i = i + 1

	temps_a_celsius(resultados_y)
	tiempos_a_minutos(resultados_t)


	return [resultados_y, resultados_t]


def runge_kutta_4(f, t0, t_fin, y0, h):
	resultados_y = []
	resultados_t = []

	t = t0
	w = y0

	resultados_y.append(w)
	resultados_t.append(t)
	i = 1
	while t <= t_fin:
		k1 = h * f(t, w)
		k2 = h * f(t + h / 2, w + k1 / 2)
		k3 = h * f(t + h / 2, w + k2 / 2)
		k4 = h * f(t + h, w + k3)

		w = w + (k1 + 2 * k2 + 2 * k3 + k4) / 6
		t = t0 + i * h
		resultados_y.append(w)
		resultados_t.append(t)
		i = i + 1


	temps_a_celsius(resultados_y)
	tiempos_a_minutos(resultados_t)


	return [resultados_y, resultados_t]



# def punto_fijo_sistema(f, x0, a_tol, n_max, j_inv, file=sys.stdout):
def punto_fijo_sistema(f, x0, n_max, j_inv, file=sys.stdout):
    x = x0
    delta = x0

    for i in range(0, n_max):
        x_old = x
        x = np.subtract(x, j_inv.dot(f(x)))

    return x

def buscar_valores_exactos(t0, t_fin, T0, CADE):
	arr_t = []
	arr_T = []

	arr_t.append(t0)
	arr_T.append(T0)

	i = 1
	t = t0
	while t < t_fin:
		t = t0 + i * CADE
		T = temperatura_exacta(T0)(t)
		arr_t.append(t)
		arr_T.append(T)
		i = i + 1

	temps_a_celsius(arr_T)
	tiempos_a_minutos(arr_t)

	return [arr_T, arr_t]

