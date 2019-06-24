import numpy as np
import sys

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

	return [resultados_y, resultados_t]


def runge_kutta_4(f, t0, t_fin, y0, h):
	resultados_y = []
	resultados_t = []

	t = t0
	w = y0

	i = 0
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

	return [resultados_y, resultados_t]



# def punto_fijo_sistema(f, x0, a_tol, n_max, j_inv, file=sys.stdout):
def punto_fijo_sistema(f, x0, n_max, j_inv, file=sys.stdout):
    x = x0
    delta = x0

    for i in range(0, n_max):
        x_old = x
        x = np.subtract(x, j_inv.dot(f(x)))

    return x
