import numpy as np

# Constantes
NP = 102145

# Propiedades del material
DENS = 7850 			# Densidad [kg / m3]
CESP = 480				# Calor Especifico [J / kg K]

# Geometria del material
D_OD = 244.48 / 1000	# Diametro externo [m]
E_WT = 13.84 / 1000		# Espesor [m]
LG_T = 12				# Longitud del tubo [m]

# Geometria del horno
LG_H = 50				# Longitud del horno [m]
NBOL = 50				# Cantidad bolsillos

# Parametros del proceso
CADE = round(-10 / 10000 * (NP - 90000) + 35) 			# Tiempo de cadencia [s]
TMP1 = round(200 / 10000 * (NP - 90000) + 500) + 273	# Temperatura [K]
TMP2 = round(200 / 10000 * (NP - 90000) + 500) + 273	# Temperatura [K] 	EJ 3: TMP1 + 40
TMP1 = 700.17916308 + 273	# Temperatura [K]
TMP2 = 554.95793595 + 273	# Temperatura [K] 	EJ 3: TMP1 + 40


# Parametros de la transferencia de calor
HCNV = 20			# Coeficiente de conveccion [W / m2 K]
SGMA = 5.6703e-8	# Constante de Stefan-Boltzmann [W / m2 K4]
EPSL = 0.85			# Factor de emisividad de la superficie del tubo

def sup_tubo():
	return np.pi * D_OD * LG_T

def velocidad():
	return LG_H / (NBOL * CADE)

def posicion(t):
	return velocidad() * t

def masa_tubo():
	return DENS * np.pi * D_OD * E_WT * (1 - E_WT / D_OD) * LG_T

def temp_horno(t): 
	if posicion(t) <= LG_H / 2:
		return TMP1
	return TMP2

def intercambio_conveccion(tiempo, temp):
	return - HCNV * sup_tubo() * (temp - temp_horno(tiempo)) / (masa_tubo() * CESP)

def intercambio_radiacion(tiempo, temp):
	return - SGMA * EPSL * sup_tubo() * (temp**4 - temp_horno(tiempo)**4) / (masa_tubo() * CESP)

def intercambio_total(tiempo, temp):
	return intercambio_radiacion(tiempo, temp) + intercambio_conveccion(tiempo, temp)


def temperatura_exacta(t0):
	return lambda t: TMP1 + (t0 - TMP1) * np.e**(-(HCNV * sup_tubo()) / (masa_tubo() * CESP) * t)




def temp_horno_5(t, tmp1, tmp2): 
	if posicion(t) <= LG_H / 2:
		return tmp1
	return tmp2

def intercambio_conveccion_5(tiempo, temp, tmp1, tmp2):
	return - HCNV * sup_tubo() * (temp - temp_horno_5(tiempo, tmp1, tmp2)) / (masa_tubo() * CESP)

def intercambio_radiacion_5(tiempo, temp, tmp1, tmp2):
	return - SGMA * EPSL * sup_tubo() * (temp**4 - temp_horno_5(tiempo, tmp1, tmp2)**4) / (masa_tubo() * CESP)

def intercambio_total_5(tiempo, temp, tmp1, tmp2):
	return intercambio_conveccion_5(tiempo, temp, tmp1 + 273, tmp2 + 273) + intercambio_radiacion_5(tiempo, temp, tmp1 + 273, tmp2 + 273)

def temperatura_exacta_5(t0):
	return lambda t: TMP1 + (t0 - TMP1) * np.e**(-(HCNV * sup_tubo()) / (masa_tubo() * CESP) * t)
