import numpy as np

def euler(f, t0, y0, h, yfin, error):
	resultados_y = []
	resultados_t = []

	w = y0
	t = t0

	resultados_y.append(w)
	resultados_t.append(t)

	i = 1
	while w < yfin - error:
	# for i in range(1, 500): 	# Limite arbitrario?
		w = w + h * f(t, w)
		t = t0 + i * h
		resultados_y.append(w)
		resultados_t.append(t)
		i = i + 1

	return [resultados_y, resultados_t]


def runge_kutta_4(f, t0, y0, h, yfin, error):
	resultados_y = []
	resultados_t = []

	t = t0
	w = y0

	i = 0
	while w < yfin - error:
		k1 = h * f(t, w)
		k2 = h * f(t + h / 2, w + k1 / 2)
		k3 = h * f(t + h / 2, w + k2 / 2)
		k4 = h * f(t + h, w + k3)

		w = w + (k1 + 2 * k2 + 2 * k3 + k4) / 6
		t = t0 + i * h
		resultados_y.append(w)
		resultados_t.append(t)
		i = i + 1

	return [resultados_y, resultados_t]