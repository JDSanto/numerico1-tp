import os
import numpy as np 
import matplotlib.pylab as plt 
import sys

from funciones import intercambio_conveccion, intercambio_total, temperatura_exacta, CADE, TMP1, TMP2, NP, temps_a_celsius, tiempos_a_minutos
from metodos import euler, runge_kutta_4, punto_fijo_sistema, buscar_valores_exactos


def buscar_intervalo_temperatura(arr, tmp, file=sys.stdout):
	pos_temp_i = -1
	for i in range(len(arr[0])):
		if arr[0][i] > tmp:
			pos_temp_i = i
			break

	if pos_temp_i < 0:
		print("Sin temperaturas en el intervalo", file=file)
		return

	print("Tk: " + str(sum(arr[0][pos_temp_i:])/len(arr[0][pos_temp_i:])), file=file)
	print("Sk: " + str(arr[1][len(arr[1]) - 1] - arr[1][pos_temp_i]), file=file)
	print("Intervalo Sk: [" + str(arr[1][pos_temp_i]) + ", " + str(arr[1][len(arr[1]) - 1]) + "]", file=file)


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
	plt.yscale('log')
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
	file = open('ej2.txt', 'w')

	T0 = 20 + 273
	t0 = 0
	t_fin = 1200
	# Optamos por usar los valores de RK

	valores_runge = runge_kutta_4(intercambio_total(TMP1, TMP2), t0, t_fin, T0, CADE)

	xx = np.linspace(t0, t_fin)
	yy = temperatura_exacta(T0)(xx)
	plt.figure(figsize=(10,7))
	tiempos_a_minutos(xx)
	temps_a_celsius(yy)
	plt.plot(xx, yy, lw=2)
	plt.plot(valores_runge[1], valores_runge[0])
	plt.xlabel('t')
	plt.ylabel('T(t)')
	plt.grid(True)
	plt.savefig('ej2.png')

	buscar_intervalo_temperatura(valores_runge, TMP2 - 10 - 273, file)

	os.chdir('../')
	print("")


def ej3():
	print("Generando Ejercicio 3...")
	os.makedirs('ej3', exist_ok=True)
	os.chdir('ej3')
	file = open('ej3.txt', 'w')

	T0 = 20 + 273
	t0 = 0
	t_fin = 1200

	# Valores de temperatura "a mano"
	tmp1 = TMP1 + 85
	tmp2 = TMP2 - 5
	valores_runge = runge_kutta_4(intercambio_total(tmp1, tmp2), t0, t_fin, T0, CADE)

	buscar_intervalo_temperatura(valores_runge, tmp2 - 10 - 273, file)

	os.chdir('../')
	file.close()
	print("")



def ej4():
	print("Generando Ejercicio 4...")
	os.makedirs('ej4', exist_ok=True)
	os.chdir('ej4')
	file = open('ej4.txt', 'w')

	T0 = 20 + 273
	t0 = 0
	t_fin = 1200

	# Valores de temperatura "a mano"
	tmp1 = TMP1 + 95
	tmp2 = TMP2 - 5
	# Es necesario cambiar el valor de la cadencia descomentando una linea en el funciones.py
	valores_runge = runge_kutta_4(intercambio_total(tmp1, tmp2), t0, t_fin, T0, CADE)


	buscar_intervalo_temperatura(valores_runge, tmp2 - 10 - 273, file)

	os.chdir('../')
	file.close()
	print("")


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

def sistema_funciones(tk_obj, sk_obj):
	def F(mat):
		tmp1 = mat.item(0)
		tmp2 = mat.item(1)
		return np.subtract(buscar_tk_sk(tmp1, tmp2), np.matrix([[tk_obj], [sk_obj]]))
	return F


def resolver_caso_ej5(sk_obj, tsk_obj, caso, file=sys.stdout):
	j_inv = np.matrix([[0.25, 0.75], [0.75, 0.25]])
	err = 1
	t0 = 0
	T0 = 20 + 273
	t_fin = 1200

	x, n_iter = punto_fijo_sistema(sistema_funciones(tsk_obj, sk_obj), sistema_funciones(tsk_obj, sk_obj)(np.matrix([[TMP1], [TMP2]])), err, j_inv)
	print('{0:4}\t{1: .14f}\t{2: .14f}\t{3: .14f}\t{4:4}'.format(sk_obj, tsk_obj, x.item(0) - 273, x.item(1) - 273, n_iter), file=file)

	valores_runge = runge_kutta_4(intercambio_total(x.item(0), x.item(1)), t0, t_fin, T0, CADE)

	xx = np.linspace(t0, t_fin)
	yy = temperatura_exacta(T0)(xx)
	plt.figure(figsize=(10,7))
	tiempos_a_minutos(xx)
	temps_a_celsius(yy)
	plt.plot(xx, yy, lw=2)
	plt.plot(valores_runge[1], valores_runge[0])
	plt.xlabel('t')
	plt.ylabel('T(t)')
	plt.grid(True)
	plt.savefig('ej5' + caso + '.png')



def ej5():
	print("Generando Ejercicio 5...")
	os.makedirs('ej5', exist_ok=True)
	os.chdir('ej5')
	file = open('ej5.txt', 'w')

	resolver_caso_ej5(10, 734.7560876525041, 'a', file)
	resolver_caso_ej5(10, round(200 / 10000 * (NP - 90000) + 550), 'b', file)
	resolver_caso_ej5(10, round(200 / 10000 * (NP - 90000) + 600), 'c', file)

	os.chdir('../')
	file.close()


ej1()
ej2()
ej3()
ej4()
ej5()
