import os
import numpy as np 
import matplotlib.pylab as plt 

from funciones import intercambio_conveccion, intercambio_total_5, intercambio_total, temperatura_exacta, CADE, TMP1, TMP2
from metodos import euler, runge_kutta_4, euler_5, runge_kutta_4_5, punto_fijo_sistema


def temps_a_celsius(arr):
	for x in range(len(arr)):
		arr[x] = arr[x] - 273 		# Kelvin a Celsius


def tiempos_a_minutos(arr):
	for x in range(len(arr)):
		arr[x] = arr[x] / 60		#intercambio_total_5 Segundos a minutos


def buscar_intervalo_temperatura(arr, tmp):
	pos_temp_i = -1
	for i in range(len(arr[0])):
		if arr[0][i] > tmp:
			pos_temp_i = i
			break

	print("Tk: " + str(sum(arr[0][pos_temp_i:])/len(arr[0][pos_temp_i:])))
	print("Intervalo Sk: [" + str(arr[1][pos_temp_i]) + ", " + str(arr[1][len(arr[1]) - 1]) + "]")


def buscar_tk_5(tmp1, tmp2):
	T0 = 20 + 273
	t0 = 0
	t_fin = 1200
	tmp = tmp2 - 10
	arr = runge_kutta_4_5(intercambio_total_5, t0, t_fin, T0, CADE, tmp1, tmp2)

	temps_a_celsius(arr[0])
	tiempos_a_minutos(arr[1])

	pos_temp_i = -1
	for i in range(len(arr[0])):
		if arr[0][i] > tmp:
			pos_temp_i = i
			break

	return sum(arr[0][pos_temp_i:])/len(arr[0][pos_temp_i:])



def buscar_sk_5(tmp1, tmp2):
	T0 = 20 + 273
	t0 = 0
	t_fin = 1200
	tmp = tmp2 - 10
	arr = runge_kutta_4_5(intercambio_total_5, t0, t_fin, T0, CADE, tmp1, tmp2)

	temps_a_celsius(arr[0])
	tiempos_a_minutos(arr[1])

	pos_temp_i = -1
	for i in range(len(arr[0])):
		if arr[0][i] > tmp:
			pos_temp_i = i
			break

	return (arr[1][len(arr[1]) - 1]) - (arr[1][pos_temp_i])



def ej1():
	print("Generando Ejercicio 1...")
	os.makedirs('ej1', exist_ok=True)
	os.chdir('ej1')

	T0 = 20 + 273
	t0 = 0
	t_fin = 1200
	valores_euler = euler(intercambio_conveccion, t0, t_fin, T0, CADE)
	valores_runge = runge_kutta_4(intercambio_conveccion, t0, t_fin, T0, CADE)
	# valores_euler = euler(intercambio_conveccion(TMP1, TMP2), t0, t_fin, T0, CADE)
	# valores_runge = runge_kutta_4(intercambio_conveccion(TMP1, TMP2), t0, t_fin, T0, CADE)
	temps_a_celsius(valores_euler[0])
	temps_a_celsius(valores_runge[0])
	tiempos_a_minutos(valores_euler[1])
	tiempos_a_minutos(valores_runge[1])

	xx = np.linspace(0, 15000)
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
	os.chdir('../')
	print("")


def ej2():
	print("Generando Ejercicio 2...")
	os.makedirs('ej2', exist_ok=True)
	os.chdir('ej2')

	T0 = 20 + 273
	t0 = 0
	t_fin = 1200
	valores_euler = euler(intercambio_total, t0, t_fin, T0, CADE)
	valores_runge = runge_kutta_4(intercambio_total, t0, t_fin, T0, CADE)

	# valores_euler = euler(intercambio_conveccion(TMP1, TMP2), t0, t_fin, T0, CADE)
	# valores_runge = runge_kutta_4(intercambio_conveccion(TMP1, TMP2), t0, t_fin, T0, CADE)
	temps_a_celsius(valores_euler[0])
	temps_a_celsius(valores_runge[0])
	tiempos_a_minutos(valores_euler[1])
	tiempos_a_minutos(valores_runge[1])

	xx = np.linspace(0, 15000)
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
	plt.savefig('ej2.png')

	print("Euler")
	buscar_intervalo_temperatura(valores_euler, TMP2 - 10 - 273)
	print("Runge Kutta 4")
	buscar_intervalo_temperatura(valores_runge, TMP2 - 10 - 273)

	os.chdir('../')
	print("")


def ej4():
	print("Generando Ejercicio 4...")

	T0 = 120 + 273
	t0 = 0
	t_fin = 1200
	valores_euler = euler(intercambio_total, t0, t_fin, T0, CADE)
	valores_runge = runge_kutta_4(intercambio_total, t0, t_fin, T0, CADE)
	# valores_euler = euler(intercambio_conveccion(TMP1, TMP2), t0, t_fin, T0, CADE)
	# valores_runge = runge_kutta_4(intercambio_conveccion(TMP1, TMP2), t0, t_fin, T0, CADE)
	temps_a_celsius(valores_euler[0])
	temps_a_celsius(valores_runge[0])
	tiempos_a_minutos(valores_euler[1])
	tiempos_a_minutos(valores_runge[1])

	print("Euler")
	buscar_intervalo_temperatura(valores_euler, TMP2 - 10 - 273)
	print("Runge Kutta 4")
	buscar_intervalo_temperatura(valores_runge, TMP2 - 10 - 273)

	print("")


def sistema_funciones(tk_obj, sk_obj):
	def F(mat):
		tmp1 = mat.item(0)
		tmp2 = mat.item(1)
		return np.matrix([[buscar_tk_5(tmp1, tmp2) - tk_obj], [buscar_sk_5(tmp1, tmp2) - sk_obj]])
	return F


def ej5():
	print("Generando Ejercicio 5...")
	
	j_inv = np.matrix([[0.25, 0.75], [0.75, 0.25]])
	punto_fijo_sistema(sistema_funciones(550, 10), sistema_funciones(550, 10)(np.matrix([[TMP1], [TMP2]])), 500, j_inv)
	# print("Generando Ejercicio 5...")
	# print(buscar_tk_5(TMP1, TMP2))
	# print(buscar_sk_5(TMP1, TMP2))

ej1()
ej2()
ej4()
ej5()
