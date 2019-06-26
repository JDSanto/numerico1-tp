import os
import numpy as np 
import matplotlib.pylab as plt 

from funciones import intercambio_conveccion, intercambio_total, temperatura_exacta, CADE, TMP1, TMP2, NP, temps_a_celsius, tiempos_a_minutos
from metodos import euler, runge_kutta_4, punto_fijo_sistema, buscar_valores_exactos


def buscar_intervalo_temperatura(arr, tmp):
	pos_temp_i = -1
	for i in range(len(arr[0])):
		if arr[0][i] > tmp:
			pos_temp_i = i
			break

	if pos_temp_i < 0:
		print("Sin temperaturas en el intervalo")
		return

	print("Tk: " + str(sum(arr[0][pos_temp_i:])/len(arr[0][pos_temp_i:])))
	print("Intervalo Sk: [" + str(arr[1][pos_temp_i]) + ", " + str(arr[1][len(arr[1]) - 1]) + "]")



def buscar_tk_sk(tmp1, tmp2):
	T0 = 20 + 273
	t0 = 0
	t_fin = 1200
	tmp = tmp2 - 10 - 273
	arr = runge_kutta_4(intercambio_total(tmp1, tmp2), t0, t_fin, T0, CADE)

	pos_temp_i = -1
	for i in range(len(arr[0])):
		if arr[0][i] > tmp:
			pos_temp_i = i
			break

	return np.matrix([[sum(arr[0][pos_temp_i:])/len(arr[0][pos_temp_i:])],
					[(arr[1][len(arr[1]) - 1]) - (arr[1][pos_temp_i])]])

def buscar_error(arr1, arr2):
	arr = []
	for i in range(len(arr1)):
		arr.append(np.abs(arr1[i] - arr2[i]))
	return arr


def ej1():
	print("Generando Ejercicio 1...")
	os.makedirs('ej1', exist_ok=True)
	os.chdir('ej1')

	T0 = 20 + 273
	t0 = 0
	t_fin = 1200
	valores_euler = euler(intercambio_conveccion(TMP1, TMP2), t0, t_fin, T0, CADE)
	valores_runge = runge_kutta_4(intercambio_conveccion(TMP1, TMP2), t0, t_fin, T0, CADE)
	valores_exactos = buscar_valores_exactos(t0, t_fin, T0, CADE)


	xx = np.linspace(t0, t_fin)
	yy = temperatura_exacta(T0)(xx)
	plt.figure(figsize=(10,7))
	tiempos_a_minutos(xx)
	temps_a_celsius(yy)
	plt.plot(xx, yy, lw=2)
	plt.plot(valores_euler[1], valores_euler[0])
	plt.plot(valores_runge[1], valores_runge[0])
	plt.xlabel('t')
	plt.ylabel('T(t)')
	plt.grid(True)
	plt.savefig('ej1.png')

	plt.figure(figsize=(10,7))
	# plt.yscale('log')
	plt.plot(valores_euler[1], buscar_error(valores_exactos[0], valores_euler[0]), 'gs', label='Euler')
	plt.plot(valores_runge[1], buscar_error(valores_exactos[0], valores_runge[0]), 'b^', label='Runge-Kutta 4')
	plt.grid(True)
	plt.savefig('ej1-error.png')

	os.chdir('../')
	print("")


def ej2():
	print("Generando Ejercicio 2...")
	os.makedirs('ej2', exist_ok=True)
	os.chdir('ej2')

	T0 = 20 + 273
	t0 = 0
	t_fin = 1200
	# Optamos por usar los valores de RK
	# valores_euler = euler(intercambio_total(TMP1, TMP2), t0, t_fin, T0, CADE)
	valores_runge = runge_kutta_4(intercambio_total(TMP1, TMP2), t0, t_fin, T0, CADE)


	xx = np.linspace(t0, t_fin)
	yy = temperatura_exacta(T0)(xx)
	plt.figure(figsize=(10,7))
	tiempos_a_minutos(xx)
	temps_a_celsius(yy)
	plt.plot(xx, yy, lw=2)
	# plt.plot(valores_euler[1], valores_euler[0])
	plt.plot(valores_runge[1], valores_runge[0])
	plt.xlabel('t')
	plt.ylabel('T(t)')
	plt.grid(True)
	plt.savefig('ej2.png')

	# buscar_intervalo_temperatura(valores_euler, TMP2 - 10 - 273)
	buscar_intervalo_temperatura(valores_runge, TMP2 - 10 - 273)

	os.chdir('../')
	print("")


def ej3():
	print("Generando Ejercicio 3...")

	T0 = 20 + 273
	t0 = 0
	t_fin = 1200

	# Valores de temperatura "a mano"
	tmp1 = TMP1 + 85
	tmp2 = TMP2 - 5
	valores_runge = runge_kutta_4(intercambio_total(tmp1, tmp2), t0, t_fin, T0, CADE)

	buscar_intervalo_temperatura(valores_runge, tmp2 - 10 - 273)

	print("")



def ej4():
	print("Generando Ejercicio 4...")

	T0 = 20 + 273
	t0 = 0
	t_fin = 1200

	# Valores de temperatura "a mano"
	tmp1 = TMP1 + 90
	tmp2 = TMP2 - 5
	valores_runge = runge_kutta_4(intercambio_total(tmp1, tmp2), t0, t_fin, T0, CADE - CADE / 20)


	buscar_intervalo_temperatura(valores_runge, tmp2 - 10 - 273)

	print("")


def sistema_funciones(tk_obj, sk_obj):
	def F(mat):
		tmp1 = mat.item(0)
		tmp2 = mat.item(1)
		return np.subtract(buscar_tk_sk(tmp1, tmp2), np.matrix([[tk_obj], [sk_obj]]))
	return F


def ej5():
	print("Generando Ejercicio 5...")

	j_inv = np.matrix([[0.25, 0.75], [0.75, 0.25]])
	n_iter = 500
	sk_obj = 10

	tsk_obj = 735.5684171924365
	x = punto_fijo_sistema(sistema_funciones(tsk_obj, sk_obj), sistema_funciones(tsk_obj, sk_obj)(np.matrix([[TMP1], [TMP2]])), n_iter, j_inv)
	print(sk_obj, tsk_obj)
	print(x.item(0) - 273, x.item(1) - 273)

	tsk_obj = round(200 / 10000 * (NP - 90000) + 550)
	x = punto_fijo_sistema(sistema_funciones(tsk_obj, sk_obj), sistema_funciones(tsk_obj, sk_obj)(np.matrix([[TMP1], [TMP2]])), n_iter, j_inv)
	print(sk_obj, tsk_obj)
	print(x.item(0) - 273, x.item(1) - 273)

	tsk_obj = round(200 / 10000 * (NP - 90000) + 600)
	x = punto_fijo_sistema(sistema_funciones(tsk_obj, sk_obj), sistema_funciones(tsk_obj, sk_obj)(np.matrix([[TMP1], [TMP2]])), n_iter, j_inv)
	print(sk_obj, tsk_obj)
	print(x.item(0) - 273, x.item(1) - 273)


ej1()
ej2()
ej3()
ej4()
ej5()
