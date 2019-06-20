import numpy as np
import sys

def bisec(f, a, b, a_tol, n_max, file=sys.stdout):

    if (f(a) * f(b) > 0):
        raise ValueError('No cumple con las condiciones para aplicar biseccion')

    r = a+(b-a)/2 
    delta = (b-a)/2

    delta_abs_graph = [] 
    
    print('{0:^4}\t{1:^17}\t{2:^17}\t{3:^17}\t{4:^17}\t{5:^17}\t{6:^17}'.format('i', 'a', 'b', 'f(a)', 'f(b)', 'ri+1', 'Δri+1'), file=file)
    print('{0:4}\t{1: .14E}\t{2: .14E}\t{3: .14E}\t{4: .14E}\t{5: .14E}'.format(0, a, b, f(a), f(b), r), file=file)
    
    for i in range(n_max):
        if f(a) * f(r) > 0:
            a = r
        else:
            b = r
        r_old = r
        r = a+(b-a)/2 
        delta = np.abs(r - r_old)
        err_porc = np.abs((r / a) * 100 - (r_old / a) * 100)
        
        delta_abs_graph.append(delta)
        
        print('{0:4}\t{1: .14E}\t{2: .14E}\t{3: .14E}\t{4: .14E}\t{5: .14E}\t{6: .14E}'.format(i + 1, a, b, f(a), f(b), r, err_porc), file=file)
        
        if delta <= a_tol:
            print('Hubo convergencia, n_iter = ' + str(i+1), file=file)
            return r, delta, i+1, delta_abs_graph
    
    raise ValueError('No hubo convergencia')
    return r, delta, i+1, delta_abs_graph



def punto_fijo(f, x0, a_tol, n_max, file=sys.stdout):
    x = x0
    delta = x0

    delta_abs_graph = []

    print('{0:^4}\t{1:^17}\t{2:^17}\t{3:^17}'.format('i', 'xn', 'Δx', 'Δx/xn'), file=file)
    print('{0:4}\t{1: .14E}'.format(0, x), file=file)

    for i in range(0, n_max):
        x_old = x
        x = x - f(x)
        err = np.abs(x - x_old)
        err_r = np.abs(x - x_old) / x

        delta = np.abs(x - x_old)

        delta_abs_graph.append(delta)

        print('{0:4}\t{1: .14E}\t{2: .14E}\t{3: .14E}'.format(i+1, x, err, err_r), file=file)

        if delta <= a_tol:
            print('Hubo convergencia, n_iter = ' + str(i+1), file=file)
            return x, delta, i+1, delta_abs_graph

    return x, delta, i+1, delta_abs_graph


def newton_raphson(f, f_d, x0, a_tol, n_max, file=sys.stdout):
    x = x0
    delta = x0

    print('{0:^4}\t{1:^17}\t{2:^17}\t{3:^17}'.format('i', 'xn', 'Δx', 'Δx/xn'), file=file)
    print('{0:4}\t{1: .14E}'.format(0, x), file=file)

    delta_abs_graph = [] 

    for i in range(0, n_max):
        x_old = x
        x = x_old - f(x_old) / f_d(x_old)
        delta = np.abs(x - x_old)
        err = np.abs(x - x_old)
        err_r = np.abs(x - x_old) / x

        delta_abs_graph.append(delta) 

        print('{0:4}\t{1: .14E}\t{2: .14E}\t{3: .14E}'.format(i+1, x, err, err_r), file=file)

        if delta <= a_tol:
            print('Hubo convergencia, n_iter = ' + str(i+1), file=file)
            return x, delta, i+1, delta_abs_graph


    return x, delta, i+1, delta_abs_graph