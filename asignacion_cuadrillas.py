import sys
#importamos el modulo cplex
import cplex
from cplex.exceptions import CplexSolverError
from recordclass import recordclass
from time import time

TOLERANCE =10e-6 
Orden = recordclass('Orden', 'id beneficio cant_trab')

class InstanciaAsignacionCuadrillas:
    def __init__(self):
        self.cantidad_trabajadores = 0
        self.cantidad_ordenes = 0
        self.ordenes = []
        self.conflictos_trabajadores = []
        self.ordenes_correlativas = []
        self.ordenes_conflictivas = []
        self.ordenes_repetitivas = []
        
    def leer_datos(self,nombre_archivo):

        # Se abre el archivo
        f = open(nombre_archivo)

        # Lectura cantidad de trabajadores
        self.cantidad_trabajadores = int(f.readline())
        
        # Lectura cantidad de ordenes
        self.cantidad_ordenes = int(f.readline())
        
        # Lectura de las ordenes
        self.ordenes = []
        for i in range(self.cantidad_ordenes):
            linea = f.readline().rstrip().split(' ')
            self.ordenes.append(Orden(linea[0],linea[1],linea[2]))
        
        # Lectura cantidad de conflictos entre los trabajadores
        cantidad_conflictos_trabajadores = int(f.readline())
        
        # Lectura conflictos entre los trabajadores
        self.conflictos_trabajadores = []
        for i in range(cantidad_conflictos_trabajadores):
            linea = f.readline().split(' ')
            self.conflictos_trabajadores.append(list(map(int,linea)))
            
        # Lectura cantidad de ordenes correlativas
        cantidad_ordenes_correlativas = int(f.readline())
        
        # Lectura ordenes correlativas
        self.ordenes_correlativas = []
        for i in range(cantidad_ordenes_correlativas):
            linea = f.readline().split(' ')
            self.ordenes_correlativas.append(list(map(int,linea)))
            
        # Lectura cantidad de ordenes conflictivas
        cantidad_ordenes_conflictivas = int(f.readline())
        
        # Lectura ordenes conflictivas
        self.ordenes_conflictivas = []
        for i in range(cantidad_ordenes_conflictivas):
            linea = f.readline().split(' ')
            self.ordenes_conflictivas.append(list(map(int,linea)))
        
        # Lectura cantidad de ordenes repetitivas
        cantidad_ordenes_repetitivas = int(f.readline())
        
        # Lectura ordenes repetitivas
        self.ordenes_repetitivas = []
        for i in range(cantidad_ordenes_repetitivas):
            linea = f.readline().split(' ')
            self.ordenes_repetitivas.append(list(map(int,linea)))
        
        # Se cierra el archivo de entrada
        f.close()


def cargar_instancia():
    # El 1er parametro es el nombre del archivo de entrada 	
    nombre_archivo1 = sys.argv[1].strip()
    # Crea la instancia vacia
    instancia = InstanciaAsignacionCuadrillas()
    # Llena la instancia con los datos del archivo de entrada 
    instancia.leer_datos(nombre_archivo1)
    return instancia

def agregar_variables(prob, instancia):
    # Definir y agregar las variables:
	# metodo 'add' de 'variables', con parametros:
	# obj: costos de la funcion objetivo
	# lb: cotas inferiores
    # ub: cotas superiores
    # types: tipo de las variables
    # names: nombre (como van a aparecer en el archivo .lp)
    cantidad_trabajadores = instancia.cantidad_trabajadores
    cantidad_ordenes = instancia.cantidad_ordenes
    cantidad_ordenes_conflictivas = len(instancia.ordenes_conflictivas)
    cantidad_ordenes_repetitivas = len(instancia.ordenes_repetitivas)
    cantidad_ordenes_correlativas = len(instancia.ordenes_correlativas)
    cant_conflictos_trabajadores = len(instancia.conflictos_trabajadores)

    conflictos_trabajadores = instancia.conflictos_trabajadores
    ordenes = instancia.ordenes
    ordenes_repetitivas = instancia.ordenes_repetitivas
    ordenes_correlativas = instancia.ordenes_correlativas

    cant_x =cantidad_ordenes * cantidad_trabajadores * 5 *6 *4
    cant_delta = cantidad_ordenes
    cant_workers = cantidad_trabajadores * 4 
    cant_tareaEnDiaYTurno = cantidad_ordenes * 5 * 6
    cant_trabajaHoy = cantidad_trabajadores * 6
    cant_deltaPago = cantidad_trabajadores * 3

    #COMENTAR PARA NO USAR LAS DESEABLES
    
    cant_conflicto = cantidad_ordenes * cantidad_trabajadores * cantidad_trabajadores
    cant_repetitivas = cantidad_trabajadores * cantidad_ordenes * cantidad_ordenes
    cant_variables = cant_x + cant_delta + cant_workers + cant_tareaEnDiaYTurno + cant_trabajaHoy +cant_deltaPago + cant_conflicto + cant_repetitivas
    
    #DESCOMENTAR PARA NO USAR LAS DESEABLES
    #cant_variables = cant_x + cant_delta + cant_workers + cant_tareaEnDiaYTurno + cant_trabajaHoy +cant_deltaPago
    
    coef_x = [0.0]*cant_x

    coef_deltas = [float(orden.beneficio) for orden in ordenes]
        
        
    coef_workers = [0.0]* cant_workers
    i = 0
    for t in range(cantidad_trabajadores):
        coef_workers[i] = -1000.0
        coef_workers[i+1] = -1200.0
        coef_workers[i+2] = -1400.0
        coef_workers[i+3] = -1500.0
        i= i+4


    coef_tareaDiaYTurno = [0.0]* cant_tareaEnDiaYTurno
    coef_trabajaHoy = [0.0]* cant_trabajaHoy
    coef_deltaPago = [0.0] * cant_deltaPago

    #COMENTAR PARA NO USAR LAS DESEABLES    
    coef_conflictos = [-21500.0] * cant_conflicto
    coef_repetitivas = [-21500.0] * cant_repetitivas
    coeficientes_funcion_objetivo = coef_x + coef_deltas + coef_workers + coef_tareaDiaYTurno + coef_trabajaHoy + coef_deltaPago + coef_conflictos + coef_repetitivas
    
    #DESCOMENTAR PARA NO USAR LAS DESEABLES
    #coeficientes_funcion_objetivo = coef_x + coef_deltas + coef_workers + coef_tareaDiaYTurno + coef_trabajaHoy + coef_deltaPago


    # Poner nombre a las variables, cotas y tipos
    tipo = ['B'] * cant_variables
    cotasup = [1] * cant_variables

    index = 0
    nombres = []

    for t in range(cantidad_ordenes):
        for w in range(cantidad_trabajadores):
            for h in range(5):
                for d in range(6):
                    for c in range(4):
                        nombres.append('x_'+str(t)+'_'+str(w)+'_'+str(h)+'_'+str(d)+'_'+str(c))
                        index += 1


    for t in range(cant_delta):
        nombres.append('delta_'+str(t))
        index += 1
        

    for w in range(cantidad_trabajadores):
        for c in range(4):
            nombres.append('worker_'+str(w)+'_'+str(c))
            tipo[index] = 'I'
            cotasup[index] = 5
            if c==3:
                cotasup[index] = max(0, cantidad_ordenes-15)
            index += 1
            
        
    for t in range(cantidad_ordenes):
        for h in range(5):
            for d in range(6):
                nombres.append('tareaEnEsteDiaYTurno_'+str(t)+'_'+str(h)+'_'+str(d))

    for w in range(cantidad_trabajadores):
        for d in range(6):
            nombres.append('trabajaHoy_'+str(w)+'_'+str(d))
        
    for w in range(cantidad_trabajadores):
        for c in range(3):
            nombres.append('deltaPago_'+str(w)+'_'+str(c))
        

    #COMENTAR PARA NO USAR LAS DESEABLES  
    
    for t in range(cantidad_ordenes):
        for w1 in range(cantidad_trabajadores):
            for w2 in range(cantidad_trabajadores):
                nombres.append('conflictos_'+str(t)+'_'+str(w1)+'_'+str(w2))
        
    for w in range(cantidad_trabajadores):
        for t1 in range(cantidad_ordenes):
            for t2 in range(cantidad_ordenes):
                nombres.append('repetitivas_'+str(w)+'_'+str(t1)+'_'+str(t2))
    
    


    # Agregar las variables
    prob.variables.add(obj=coeficientes_funcion_objetivo, lb=[0] * cant_variables, ub=cotasup,
                       types=tipo, names=nombres)



def agregar_restricciones(prob, instancia):
    cantidad_trabajadores = instancia.cantidad_trabajadores
    cantidad_ordenes = instancia.cantidad_ordenes
    cantidad_ordenes_conflictivas = len(instancia.ordenes_conflictivas)
    cantidad_ordenes_repetitivas = len(instancia.ordenes_repetitivas)
    cantidad_ordenes_correlativas = len(instancia.ordenes_correlativas)
    cant_conflictos_trabajadores = len(instancia.conflictos_trabajadores)

    cant_x =cantidad_ordenes * cantidad_trabajadores * 5 *6 *4
    cant_delta = cantidad_ordenes
    cant_workers = cantidad_trabajadores * 4 
    cant_tareaEnDiaYTurno = cantidad_ordenes * 5 * 6
    cant_trabajaHoy = cantidad_trabajadores * 6
    cant_deltaPago = cantidad_trabajadores * 3
    cant_conflicto = cantidad_ordenes * cantidad_trabajadores * cantidad_trabajadores
    cant_repetitivas = cantidad_trabajadores * cantidad_ordenes * cantidad_ordenes

    #COMENTAR PARA NO USAR LAS DESEABLES
    cant_variables = cant_x + cant_delta + cant_workers + cant_tareaEnDiaYTurno + cant_trabajaHoy +cant_deltaPago + cant_conflicto + cant_repetitivas
    
    #DESCOMENTAR PARA NO USAR LAS DESEABLES
    #cant_variables = cant_x + cant_delta + cant_workers + cant_tareaEnDiaYTurno + cant_trabajaHoy +cant_deltaPago
    
 
    variables = list(range(cant_variables))
    X = [[[[[None for _ in range(4)] for _ in range(6)] for _ in range(5)] for _ in range(cantidad_trabajadores)] for _ in range(cantidad_ordenes)]
    index = 0
    for o in range(cantidad_ordenes):
        for t in range(cantidad_trabajadores):
            for i in range(5):
                for j in range(6):
                    for g in range(4):
                        X[o][t][i][j][g] = variables[index]
                        index += 1


    delta = [0] * cantidad_ordenes
    for t in range(cantidad_ordenes):
        delta[t] = variables[index]
        index += 1 

    workers = [[None for _ in range(4)] for _ in range(cantidad_trabajadores)]
    for w in range(cantidad_trabajadores):
        for c in range(4):
            workers[w][c] = variables[index]
            index += 1
    
    tareaEnEsteDiaYTurno = [[[None for _ in range(6)] for _ in range(5)] for _ in range(cantidad_ordenes)]
    for t in range(cantidad_ordenes):
        for h in range(5):
            for d in range(6):
                tareaEnEsteDiaYTurno[t][h][d] = variables[index]
                index += 1

    trabajaHoy = [[None for _ in range(6)] for _ in range(cantidad_trabajadores)]
    for w in range(cantidad_trabajadores):
        for d in range(6):
            trabajaHoy[w][d] = variables[index]
            index += 1
    
    deltaPago = [[None for _ in range(3)] for _ in range(cantidad_trabajadores)]
    for w in range(cantidad_trabajadores):
        for c in range(3):
            deltaPago[w][c] = variables[index]
            index += 1


    #COMENTAR PARA NO USAR LAS DESEABLES
    
    conflicto = [[[None for _ in range(cantidad_trabajadores)] for _ in range(cantidad_trabajadores)] for _ in range(cantidad_ordenes)]
    for t in range(cantidad_ordenes):
        for w1 in range(cantidad_trabajadores):
            for w2 in range(cantidad_trabajadores):
                conflicto[t][w1][w2] = variables[index]
                index += 1

    repetitivas = [[[None for _ in range(cantidad_ordenes)] for _ in range(cantidad_ordenes)] for _ in range(cantidad_trabajadores)]
    for w in range(cantidad_trabajadores):
        for t1 in range(cantidad_ordenes):
            for t2 in range(cantidad_ordenes):
                repetitivas[w][t1][t2] = variables[index]
                index += 1
    


    ordenes = instancia.ordenes
    tareas_correlativas = instancia.ordenes_correlativas
    ordenes_conflictivas = instancia.ordenes_conflictivas
    conflictos_trabajadores = instancia.conflictos_trabajadores
    ordenes_repetitivas = instancia.ordenes_repetitivas


    # Matcheo sumatoria de X a los workers
    for w in range(cantidad_trabajadores):
        for g in range(4):
            valores = [] 
            indices = []
            indices.append(workers[w][g])
            valores.append(1)
            for d in range(6):
                for t in range(cantidad_ordenes):
                    for h in range(5):
                        indices.append(X[t][w][h][d][g])
                        valores.append(-1)
            fila = [indices,valores]
            prob.linear_constraints.add(lin_expr=[fila], senses=['E'], rhs=[0], names=[f'Restriccion_para_w_{w}_c_{g}'])


    # Restriccion 1 lado izq
    for t in range(cantidad_ordenes):
        indices = []
        valores = []

        indices.append(delta[t])
        valores.append(1)

        for w in range(cantidad_trabajadores):
            for h in range(5):
                for d in range(6):
                    for g in range(4):
                        indices.append(X[t][w][h][d][g])
                        valores.append(-1)

        fila = [indices, valores]
    
        
        prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_1_lado_izq_t_{t}'])

       
    # Restriccion 1 lado der

    for t in range(cantidad_ordenes):
        indices = []
        valores = []
        indices.append(delta[t])
        valores.append(-int(ordenes[t].cant_trab))

        for w in range(cantidad_trabajadores):
            for h in range(5):
                for d in range(6):
                    for g in range(4):
                        indices.append(X[t][w][h][d][g])
                        valores.append(1) 

        fila = [indices,valores]
        prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_1_lado_der_t_{t}'])

    # Restriccion 2 lado izq
    
    for t in range(cantidad_ordenes):
        for h in range(5):
            for d in range(6):
                indices = []
                valores = []
                indices.append(tareaEnEsteDiaYTurno[t][h][d])
                valores.append(1)  

                for w in range(cantidad_trabajadores):
                    for g in range(4):
                        indices.append(X[t][w][h][d][g])
                        valores.append(-1) 

                fila = [indices,valores]
                prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_2_lado_izq_t_{t}_h_{h}_d_{d}'])

    # Restriccion 2 lado der

    for t in range(cantidad_ordenes):
        for h in range(5):
            for d in range(6):
                valores = []
                indices = []
                indices.append(tareaEnEsteDiaYTurno[t][h][d])
                valores.append(-int(ordenes[t].cant_trab))

                for w in range(cantidad_trabajadores):
                    for g in range(4):
                        indices.append(X[t][w][h][d][g])
                        valores.append(1) 

                fila = [indices,valores]
                prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_2_lado_der_t_{t}_h_{h}_d_{d}'])
        
    # Restriccion 3
    
    for t in range(cantidad_ordenes):
        valores = []
        indices = []
        indices.append(delta[t])
        valores.append(1)  

        for h in range(5):
            for d in range(6):
                indices.append(tareaEnEsteDiaYTurno[t][h][d])
                valores.append(-1)  

        fila = [indices,valores]
        prob.linear_constraints.add(lin_expr=[fila], senses=['E'], rhs=[0], names=[f'Restriccion_3_t_{t}'])
     
    # Restriccion 4
    
    for t in range(cantidad_ordenes):
        for h in range(5):
            for d in range(6):
                valores = []
                indices = []
                indices.append(tareaEnEsteDiaYTurno[t][h][d])
                valores.append(int(ordenes[t].cant_trab))

                for w in range(cantidad_trabajadores):
                    for g in range(4):
                        indices.append(X[t][w][h][d][g])
                        valores.append(-1)

                fila = [indices,valores]
                prob.linear_constraints.add(lin_expr=[fila], senses=['E'], rhs=[0], names=[f'Restriccion_4_t_{t}_h_{h}_d_{d}'])
           
    # Restriccion 5
    
    for t in range(cantidad_ordenes):
        for w in range(cantidad_trabajadores):
            for h in range(5):
                for d in range(6):
                    for g in range(4):
                        valores = [] 
                        indices = []
                        indices.append(X[t][w][h][d][g])
                        valores.append(1)
                    fila = [indices,valores]
                    prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Restriccion_5_t_{t}_w_{w}_h_{h}_d_{d}'])

# Restriccion 6

    for w in range(cantidad_trabajadores):
        for h in range(5):
            for d in range(6):
                for g in range(4):
                    for t in range(cantidad_ordenes):
                        valores = [] 
                        indices = []
                        indices.append(X[t][w][h][d][g])
                        valores.append(1)
                    fila = [indices,valores]
                    prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Restriccion_6_w_{w}_h_{h}_d_{d}_c_{g}'])

# Restriccion 7
     
    for t in range(cantidad_ordenes):
        for w in range(cantidad_trabajadores):
            for g in range(4):
                for d in range(6):
                    for h in range(5):
                        valores = [] 
                        indices = []
                        indices.append(X[t][w][h][d][g])
                        valores.append(1)
                fila = [indices,valores]
                prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Restriccion_7_t_{t}_w_{w}_c_{g}'])


# Restriccion 8.1 lado izq
    
    for d in range(6):
        for w in range(cantidad_trabajadores):
            valores = [] 
            indices = []
            indices.append(trabajaHoy[w][d])
            valores.append(1)
            for g in range(4):
                for t in range(cantidad_ordenes):
                    for h in range(5):
                        indices.append(X[t][w][h][d][g])
                        valores.append(-1)
            fila = [indices,valores]
            prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_8.1_lado_izq_w_{w}_d_{d}'])


# Restriccion 8.1 lado der
     
    for d in range(6):
        for w in range(cantidad_trabajadores):
            valores = [] 
            indices = []
            indices.append(trabajaHoy[w][d])
            valores.append(1)
            for g in range(4):
                for t in range(cantidad_ordenes):
                    for h in range(5):
                        indices.append(X[t][w][h][d][g])
                        valores.append(-1)
            fila = [indices,valores]
            prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_8.1_lado_der_w_{w}_d_{d}'])

# Restriccion 8.2
     
    for w in range(cantidad_trabajadores):
        valores = [] 
        indices = []
        for d in range(6):
            indices.append(trabajaHoy[w][d])
            valores.append(-4)
        fila = [indices,valores]
        prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[5], names=[f'Restriccion_8.2_w_{w}'])

# Restriccion 9
 
    for d in range(6):
        for w in range(cantidad_trabajadores):
            for g in range(4):
                for t in range(cantidad_ordenes):
                    for h in range(5):
                        valores = [] 
                        indices = []
                        indices.append(X[t][w][h][d][g])
                        valores.append(1)
            fila = [indices,valores]
            prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[4], names=[f'Restriccion_7_d_{d}_w_{w}'])


    

# Restriccion 10.1
    for w in range(cantidad_trabajadores):
        for d in range(6):
            for h in range(4):
                for conf in ordenes_conflictivas:
                    indices = []
                    valores = []
                    seen_indices = set()
                    A, B = conf
                    for g1 in range(4):
                        if X[A][w][h][d][g1] not in seen_indices:
                            indices.append(X[A][w][h][d][g1])
                            valores.append(1) 
                            seen_indices.add(X[A][w][h][d][g1])   
                    for g2 in range(4):
                        if X[B][w][h][d][g2] not in seen_indices:    
                            indices.append(X[B][w][h][d][g2])
                            valores.append(1) 
                            seen_indices.add(X[B][w][h][d][g2])

                    fila = [indices,valores]
                    prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Restriccion_10.1_w_{w}_h_{h}_d_{d}_tareaconfAB_{A}_{B}'])



# Restriccion 10.2
    for w in range(cantidad_trabajadores):
        for d in range(6):
            for h in range(4):
                for conf in ordenes_conflictivas:
                    indices = []
                    valores = []
                    seen_indices = set()
                    A, B = conf
                    for g1 in range(4):
                        if X[A][w][h][d][g1] not in seen_indices:
                            indices.append(X[B][w][h][d][g1])
                            valores.append(1) 
                            seen_indices.add(X[B][w][h][d][g1])   
                    for g2 in range(4):
                        if X[B][w][h][d][g2] not in seen_indices:    
                            indices.append(X[A][w][h][d][g2])
                            valores.append(1) 
                            seen_indices.add(X[A][w][h][d][g2])

                    fila = [indices,valores]
                    prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Restriccion_10.2_w_{w}_h{h}_d{d}_tareaconfAB_{A}_{B}'])



# Restriccion 11
    for h in range(4):
        for d in range(6):
            for correlativas in tareas_correlativas:
                indices = []
                valores = []
                seen_indices = set()
                A, B = correlativas
                for g1 in range(4):
                    for w1 in range(cantidad_trabajadores):
                        if X[A][w1][h][d][g1] not in seen_indices:
                            indices.append(X[A][w1][h][d][g1])
                            valores.append(1)
                            seen_indices.add(X[A][w1][h][d][g1])
                for g2 in range(4):
                    for w2 in range(cantidad_trabajadores):
                        if X[B][w2][h+1][d][g2] not in seen_indices:
                            indices.append(X[B][w2][h+1][d][g2])
                            valores.append(1)
                            seen_indices.add(X[B][w2][h+1][d][g2])
                        

                fila = [indices,valores]
                prob.linear_constraints.add(lin_expr=[fila], senses=['E'], rhs=[0], names=[f'Restriccion_11_h_{h}_d{d}_tareacorrelAB_{A}_{B}'])

# Restriccion 12 lado izq

    for w1 in range(cantidad_trabajadores):
            if(cantidad_trabajadores >1):
                for w2 in range(cantidad_trabajadores):
                    valores = [] 
                    indices = []
                    seen_indices = set()
                    for t1 in range(cantidad_ordenes):
                        for d1 in range(6):
                            for h1 in range(5):
                                for g1 in range(4):
                                    if X[t1][w1][h1][d1][g1] not in seen_indices:
                                        indices.append(X[t1][w1][h1][d1][g1])
                                        valores.append(-1)
                                        seen_indices.add(X[t1][w1][h1][d1][g1])
                if(cantidad_trabajadores >1):
                    for t2 in range(cantidad_ordenes):
                        for d2 in range(6):
                            for h2 in range(5):
                                for g2 in range(4):
                                    if X[t2][w2][h2][d2][g2] not in seen_indices:
                                        indices.append(X[t2][w2][h2][d2][g2])
                                        valores.append(1)
                                        seen_indices.add(X[t2][w2][h2][d2][g2])

                    fila = [indices,valores]
                    prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[8], names=[f'Restriccion_12_izq_w1_{w1}w2{w2}'])


# Restriccion 12 lado der

    for w1 in range(cantidad_trabajadores):
            if(cantidad_trabajadores >1):
                for w2 in range(cantidad_trabajadores):
                    valores = [] 
                    indices = []
                    seen_indices = set()
                    for t1 in range(cantidad_ordenes):
                        for d1 in range(6):
                            for h1 in range(5):
                                for g1 in range(4):
                                    if X[t1][w1][h1][d1][g1] not in seen_indices:
                                        indices.append(X[t1][w1][h1][d1][g1])
                                        valores.append(1)
                                        seen_indices.add(X[t1][w1][h1][d1][g1])
                if(cantidad_trabajadores>1):
                    for t2 in range(cantidad_ordenes):
                        for d2 in range(6):
                            for h2 in range(5):
                                for g2 in range(4):
                                    if X[t2][w2][h2][d2][g2] not in seen_indices:
                                        indices.append(X[t2][w2][h2][d2][g2])
                                        valores.append(-1)
                                        seen_indices.add(X[t2][w2][h2][d2][g2])

                    fila = [indices,valores]
                    prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[8], names=[f'Restriccion_12_der_w1_{w1}w2{w2}'])
   # Restriccion 13.1.a
    
    for w in range(cantidad_trabajadores):
        valores = [] 
        indices = []
        indices.append(deltaPago[w][0])
        valores.append(5)
        indices.append(workers[w][0])
        valores.append(-1)                
        fila = [indices,valores]
        prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_13.1.a_w_{w}'])
    
# Restriccion 13.1.b
    
    for w in range(cantidad_trabajadores):
        valores = [] 
        indices = []
        indices.append(workers[w][0])
        valores.append(1)                
        fila = [indices,valores]
        prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[5], names=[f'Restriccion_13.1.b_w_{w}'])

    
# Restriccion 13.2.a
    
    for w in range(cantidad_trabajadores):
        valores = [] 
        indices = []
        indices.append(deltaPago[w][1])
        valores.append(5)
        indices.append(workers[w][1])
        valores.append(-1)                
        fila = [indices,valores]
        prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_13.2.a_w_{w}'])

# Restriccion 13.2.b
    
    for w in range(cantidad_trabajadores):
        valores = [] 
        indices = []
        indices.append(workers[w][1])
        valores.append(1)  
        indices.append(deltaPago[w][0])
        valores.append(-5)              
        fila = [indices,valores]
        prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_13.2.b_w_{w}'])



# Restriccion 13.3.a

    for w in range(cantidad_trabajadores):
        valores = [] 
        indices = []
        indices.append(deltaPago[w][2])
        valores.append(5)
        indices.append(workers[w][2])
        valores.append(-1)                
        fila = [indices,valores]
        prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_13.3.a_w_{w}'])


# Restriccion 13.3.b

    for w in range(cantidad_trabajadores):
        valores = [] 
        indices = []
        indices.append(workers[w][2])
        valores.append(1)  
        indices.append(deltaPago[w][1])
        valores.append(-5)              
        fila = [indices,valores]
        prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_13.3.b_w_{w}'])

        
# Restriccion 13.4.a

    for w in range(cantidad_trabajadores):
        valores = [] 
        indices = []
        indices.append(workers[w][3])
        valores.append(-1)                
        fila = [indices,valores]
        prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_13.4.a_w_{w}'])

# Restriccion 13.4.b

    for w in range(cantidad_trabajadores):
        valores = [] 
        indices = []
        indices.append(workers[w][3])
        valores.append(1)  
        indices.append(deltaPago[w][2])
        valores.append(-cantidad_ordenes)              
        fila = [indices,valores]
        prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_13.4.b_w_{w}'])
    

    #COMENTAR PARA NO USAR LAS DESEABLES (restricciones 14 y 15 completas)


# Restriccion 14.1
    for t in range(cantidad_ordenes):
        for conf in conflictos_trabajadores:
            indices = []
            valores = []
            seen_indices = set()
            A, B = conf
            indices.append(conflicto[t][A][B])
            valores.append(-1)
            for d in range(6):
                for h in range(5):    
                    for g1 in range(4):
                        if X[t][A][h][d][g1] not in seen_indices:
                            indices.append(X[t][A][h][d][g1])
                            valores.append(1)
                            seen_indices.add(X[t][A][h][d][g1])
                    for g2 in range(4):
                        if X[t][B][h][d][g2] not in seen_indices:
                            indices.append(X[t][B][h][d][g2])
                            valores.append(1)
                            seen_indices.add(X[t][B][h][d][g2])       

            fila = [indices,valores]
            prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Restriccion_14.1_t_{t}_confTrab_{A}_{B}'])


# Restriccion 14.2.
    for t in range(cantidad_ordenes):
        for conf in conflictos_trabajadores:
            indices = []
            valores = []
            seen_indices = set()
            A, B = conf
            indices.append(conflicto[t][A][B])
            valores.append(2)
            for d in range(6):
                for h in range(5):    
                    for g1 in range(4):
                        if X[t][A][h][d][g1] not in seen_indices:
                            indices.append(X[t][A][h][d][g1])
                            valores.append(-1)
                            seen_indices.add(X[t][A][h][d][g1])
                    for g2 in range(4):
                        if X[t][B][h][d][g2] not in seen_indices:
                            indices.append(X[t][B][h][d][g2])
                            valores.append(-1)
                            seen_indices.add(X[t][B][h][d][g2])       

            fila = [indices,valores]
            prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_14.2_t_{t}_confTrab_{A}_{B}'])


# Restriccion 15.1
    for w in range(cantidad_trabajadores):
        for rep in ordenes_repetitivas:
            indices = []
            valores = []
            seen_indices = set()
            A, B = rep
            indices.append(repetitivas[w][A][B])
            valores.append(-1)
            for d in range(6):
                for h in range(5):    
                    for g1 in range(4):
                        if X[A][w][h][d][g1] not in seen_indices:
                            indices.append(X[A][w][h][d][g1])
                            valores.append(1)
                            seen_indices.add(X[A][w][h][d][g1])
                    for g2 in range(4):
                        if X[B][w][h][d][g2] not in seen_indices:
                            indices.append(X[B][w][h][d][g2])
                            valores.append(1)
                            seen_indices.add(X[B][w][h][d][g2])       

            fila = [indices,valores]
            prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Restriccion_15.1_w_{w}_tareaRep_{A}_{B}'])


# Restriccion 15.2.
    for w in range(cantidad_trabajadores):
        for rep in ordenes_repetitivas:
            indices = []
            valores = []
            seen_indices = set()
            A, B = rep
            indices.append(repetitivas[w][A][B])
            valores.append(2)
            for d in range(6):
                for h in range(5):    
                    for g1 in range(4):
                        if X[A][w][h][d][g1] not in seen_indices:
                            indices.append(X[A][w][h][d][g1])
                            valores.append(-1)
                            seen_indices.add(X[A][w][h][d][g1])
                    for g2 in range(4):
                        if X[B][w][h][d][g2] not in seen_indices:
                            indices.append(X[B][w][h][d][g2])
                            valores.append(-1)
                            seen_indices.add(X[B][w][h][d][g2])       

            fila = [indices,valores]
            prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Restriccion_15.2_w_{w}_tareaRep_{A}_{B}'])
    
    


def armar_lp(prob, instancia):

    # Agregar las variables
    agregar_variables(prob, instancia)
   
    # Agregar las restricciones 
    agregar_restricciones(prob, instancia)

    # Setear el sentido del problema
    prob.objective.set_sense(prob.objective.sense.maximize)

    # Escribir el lp a archivo
    
    prob.write('asignacionCuadrillas.lp')

def resolver_lp(prob):
    
    # Definir los parametros del solver
    prob.parameters.mip.tolerances.mipgap.set(1e-10)
       
    # Resolver el lp
    try:
        prob.solve()
    except CplexSolverError as exception:
        print("Fallo por ", exception )


def mostrar_solucion(prob,instancia):
    # Obtener informacion de la solucion a traves de 'solution'
    
    # Tomar el estado de la resolucion
    status = prob.solution.get_status_string(status_code = prob.solution.get_status())
    
    # Tomar el valor del funcional
    valor_obj = prob.solution.get_objective_value()

    nombres_variables = prob.variables.get_names()
    
    print('Funcion objetivo: ',valor_obj,'(' + str(status) + ')')
    
    # Tomar los valores de las variables
    x  = prob.solution.get_values()

    '''
    for t in range(instancia.cantidad_ordenes):
        if x[index] > TOLERANCE:
            print(f'delta_{t}: {x[index]}')
        index += 1

    for w in range(instancia.cantidad_trabajadores):
        for c in range(4):
            if x[index] > TOLERANCE:
                print(f'worker_{w}_{c}: {x[index]}')
            index += 1

    for t in range(instancia.cantidad_ordenes):
        for h in range(5):
            for d in range(6):
                if x[index] > TOLERANCE:
                    print(f'tareaEnEsteDiaYTurno_{t}_{h}_{d}: {x[index]}')
                index += 1

    for w in range(instancia.cantidad_trabajadores):
        for d in range(6):
            if x[index] > TOLERANCE:
                print(f'trabajaHoy_{w}_{d}: {x[index]}')
            index += 1

    for w in range(instancia.cantidad_trabajadores):
        for c in range(3):
            if x[index] > TOLERANCE:
                print(f'deltaPago_{w}_{c}: {x[index]}')
            index += 1
    
    # Comentar para usar las deseables
    '''
    '''
    for t in range(instancia.cantidad_ordenes):
        for w1 in range(instancia.cantidad_trabajadores):
            for w2 in range(instancia.cantidad_trabajadores):
                if x[index] > TOLERANCE:
                    print(f'conflictos_{t}_{w1}_{w2}: {x[index]}')
                index += 1

    for w in range(instancia.cantidad_trabajadores):
        for t1 in range(instancia.cantidad_ordenes):
            for t2 in range(instancia.cantidad_ordenes):
                if x[index] > TOLERANCE:
                    print(f'repetitivas_{w}_{t1}_{t2}: {x[index]}')
                index += 1
    '''

def escribir_solucion(prob,instancia, creation_time, execution_time):
    
    # Tomar los valores de las variables
    x  = prob.solution.get_values()
    # Mostrar las variables con valor positivo (mayor que una tolerancia)
    
    
    index = 0
    with open("nuestra_instancia_valores.txt", "w") as file:
        status = prob.solution.get_status_string(status_code = prob.solution.get_status())
        valor_obj = prob.solution.get_objective_value()    
        file.write('Funcion objetivo: '+str(valor_obj)+'(' + str(status) + ')\n\n')

        file.write("\n** Creation Runtime:"+
            str(int((creation_time/3600)))+":"+str(int((creation_time%3600)/60))+":"
            +str(int((creation_time%3600)%60)) )
        file.write("\n** Execution Default Runtime:"+
            str(int((execution_time/3600)))+":"+str(int((execution_time%3600)/60))+":"
            +str(int((execution_time%3600)%60))+ "\n\n")
        
        for t in range(instancia.cantidad_ordenes):
            for w in range(instancia.cantidad_trabajadores):
                for h in range(5):
                    for d in range(6):
                        for c in range(4):
                            if x[index] > TOLERANCE:
                                file.write(f'La tarea {t}, el trabajador {w}, el horario {h}, el dia {d}, rango salarial {c}: {x[index]}\n')
                                #print(f'La tarea {t}, el trabajador {w}, el horario {h}, el día {d}, rango salarial {c}: {x[index]}')
                            index += 1


        # COMENTAR PARA NO USAR LAS DESEABLES
        
        index += instancia.cantidad_ordenes + instancia.cantidad_trabajadores * 4 + instancia.cantidad_ordenes * 5 * 6 + instancia.cantidad_trabajadores * 6 + instancia.cantidad_trabajadores * 3
        
        for t in range(instancia.cantidad_ordenes):
            for w1 in range(instancia.cantidad_trabajadores):
                for w2 in range(instancia.cantidad_trabajadores):
                    if x[index] > TOLERANCE:
                        file.write(f'En la tarea {t} conflicto entre el trabajador {w1} y el trabajador {w2}: {x[index]}\n')
                    index += 1
        file.write('\n')
        for w in range(instancia.cantidad_trabajadores):
            for t1 in range(instancia.cantidad_ordenes):
                for t2 in range(instancia.cantidad_ordenes):
                    if x[index] > TOLERANCE:
                        file.write(f'El trabajador {w} hace las tareas repetitivas {t1} y {t2}: {x[index]}\n')
                    index += 1
        


def main():
    #with open("tiempos_nuestra_instancia.txt", "w") as file:
        start_time = time()
        # Lectura de datos desde el archivo de entrada
        instancia = cargar_instancia()
        
        # Definicion del problema de Cplex
        prob = cplex.Cplex()
        
        # Definicion del modelo
        armar_lp(prob,instancia)
        finish_armar_time = time()
        creation_time = finish_armar_time - start_time

        print("\n** Creation Runtime:",
            str(int((creation_time/3600)))+":"+str(int((creation_time%3600)/60))+":"
            +str(int((creation_time%3600)%60)) )
        #file.write("\n** Creation Runtime:"+
        #    str(int((creation_time/3600)))+":"+str(int((creation_time%3600)/60))+":"
        #    +str(int((creation_time%3600)%60)) )

        start_resolver_time = time()

        # Resolucion del modelo
        resolver_lp(prob)

        # Obtencion de la solucion
        mostrar_solucion(prob,instancia)

        end_resolver_time = time()

        execution_time = end_resolver_time - start_resolver_time

        
        print("\n** Execution Default Runtime:",
            str(int((execution_time/3600)))+":"+str(int((execution_time%3600)/60))+":"
            +str(int((execution_time%3600)%60)) )
        #file.write("\n** Execution Default Runtime:"+
        #    str(int((execution_time/3600)))+":"+str(int((execution_time%3600)/60))+":"
        #    +str(int((execution_time%3600)%60)) )
        
        escribir_solucion(prob, instancia, creation_time, execution_time)
        
        '''


        prob = cplex.Cplex()
        armar_lp(prob,instancia)

        start_second_time = time()
        prob.parameters.mip.strategy.nodeselect.set(0)
        resolver_lp(prob)
        mostrar_solucion(prob,instancia)
        dfs_time = time() - start_second_time

        print("\n** Depth-first search time (nodeselect): ", str(int((dfs_time/3600)))+":"+str(int((dfs_time%3600)/60))+":"
            +str(int((dfs_time%3600)%60)) )
        print("\n** Depth-first search time (nodeselect): ", dfs_time)
        prob.parameters.mip.strategy.nodeselect.set(1)
        file.write("\n** Depth-first search time (nodeselect): "+ str(int((dfs_time/3600)))+":"+str(int((dfs_time%3600)/60))+":"
            +str(int((dfs_time%3600)%60)) )


        prob = cplex.Cplex()
        armar_lp(prob,instancia)
        start_pseudocosto_time = time()
        prob.parameters.mip.strategy.variableselect.set(2)
        resolver_lp(prob)
        mostrar_solucion(prob,instancia)
        pseudocosto_time = time() - start_pseudocosto_time

        print("\n** Pseudocosto time (variableselect): ", str(int((pseudocosto_time/3600)))+":"+str(int((pseudocosto_time%3600)/60))+":"
            +str(int((pseudocosto_time%3600)%60)) )
        print("\n** Pseudocosto time (nodeselect): ", pseudocosto_time)
        prob.parameters.mip.strategy.variableselect.set(0)
        file.write("\n** Pseudocosto time (variableselect): "+ str(int((pseudocosto_time/3600)))+":"+str(int((pseudocosto_time%3600)/60))+":"
            +str(int((pseudocosto_time%3600)%60)) )


        prob = cplex.Cplex()
        armar_lp(prob,instancia)
        start_strongbranching_time = time()
        prob.parameters.mip.strategy.variableselect.set(3)
        resolver_lp(prob)
        mostrar_solucion(prob,instancia)
        strongbranching_time = time() -  start_strongbranching_time

        print("\n** Strong branching time (variableselect): ", str(int((strongbranching_time/3600)))+":"+str(int((strongbranching_time%3600)/60))+":"
            +str(int((strongbranching_time%3600)%60)) )
        print("\n** Strong branching time (nodeselect): ", strongbranching_time)
        prob.parameters.mip.strategy.variableselect.set(0)
        file.write("\n** Strong branching time (variableselect): "+ str(int((strongbranching_time/3600)))+":"+str(int((strongbranching_time%3600)/60))+":"
            +str(int((strongbranching_time%3600)%60)) )


        prob = cplex.Cplex()
        armar_lp(prob,instancia)
        start_preprocesamiento_time = time()
        prob.parameters.preprocessing.presolve.set(0)
        resolver_lp(prob)
        mostrar_solucion(prob,instancia)
        preprocesamiento_time = time() -  start_preprocesamiento_time

        print("\n** Preprosesamiento time (variableselect): ", str(int((preprocesamiento_time/3600)))+":"+str(int((preprocesamiento_time%3600)/60))+":"
            +str(int((preprocesamiento_time%3600)%60)) )
        print("\n**  Preprosesamiento time: ", preprocesamiento_time)
        file.write("\n** Preprosesamiento time (variableselect): "+ str(int((preprocesamiento_time/3600)))+":"+str(int((preprocesamiento_time%3600)/60))+":"
            +str(int((preprocesamiento_time%3600)%60)) )

        prob.parameters.preprocessing.presolve.set(1)



        prob = cplex.Cplex()
        armar_lp(prob,instancia)
        start_conheuristica_time = time()
        prob.parameters.mip.strategy.heuristiceffort.set(3)
        resolver_lp(prob)
        mostrar_solucion(prob,instancia)
        conheuristica_time = time() -  start_conheuristica_time

        print("\n** Con mas heuristicas time: ", str(int((conheuristica_time/3600)))+":"+str(int((conheuristica_time%3600)/60))+":"
            +str(int((conheuristica_time%3600)%60)) )
        
        print("\n** Con mas heuristicas time: ", conheuristica_time)
        file.write("\n** Con mas heuristicas time: "+ str(int((conheuristica_time/3600)))+":"+str(int((conheuristica_time%3600)/60))+":"
            +str(int((conheuristica_time%3600))))

        prob.parameters.mip.strategy.heuristiceffort.set(1)



        prob = cplex.Cplex()
        armar_lp(prob,instancia)
        start_sin_cortes_time = time()
        prob.parameters.mip.limits.cutpasses.set(-1)
        resolver_lp(prob)
        mostrar_solucion(prob,instancia)
        termina_sin_cortes_time = time() - start_sin_cortes_time

        print("\n** Termina de ejecutar sin los cortes en la raiz time: ", str(int((termina_sin_cortes_time/3600)))+":"+str(int((termina_sin_cortes_time%3600)/60))+":"
            +str(int((termina_sin_cortes_time%3600)%60)) )
        print("\n** Termina de ejecutar sin los cortes en la raiz time: ", termina_sin_cortes_time)
        file.write("\n** Termina de ejecutar sin los cortes en la raiz time "+ str(int((termina_sin_cortes_time/3600)))+":"+str(int((termina_sin_cortes_time%3600)/60))+":"
            +str(int((termina_sin_cortes_time%3600)%60)))

        prob.parameters.mip.limits.cutpasses.set(0)


        prob = cplex.Cplex()
        armar_lp(prob,instancia)
        start_sin_cortesenarbol_time = time()
        prob.parameters.mip.cuts.nodecuts.set(-1)
        resolver_lp(prob)
        mostrar_solucion(prob,instancia)
        termina_sin_cortesenarbol_time = time() - start_sin_cortesenarbol_time

        print("\n** Termina de ejecutar sin los cortes en los nodos time: ", str(int((termina_sin_cortesenarbol_time/3600)))+":"+str(int((termina_sin_cortesenarbol_time%3600)/60))+":"
            +str(int((termina_sin_cortesenarbol_time%3600)%60)) )
        print("\n** Termina de ejecutar sin los cortes en los nodos time: ", termina_sin_cortesenarbol_time)
        file.write("\n** Termina de ejecutar sin los cortes en los nodos time: "+ str(int((termina_sin_cortesenarbol_time/3600)))+":"+str(int((termina_sin_cortesenarbol_time%3600)/60))+":"
            +str(int((termina_sin_cortesenarbol_time%3600)%60)))

        prob.parameters.mip.limits.cutpasses.set(0)


        tiempo_total = time() - start_time
        print("\n** Tiempo total: "+ str(int((tiempo_total/3600)))+":"+str(int((tiempo_total%3600)/60))+":"
            +str(int((tiempo_total%3600)%60)))
        file.write("\n** Tiempo total: "+ str(int((tiempo_total/3600)))+":"+str(int((tiempo_total%3600)/60))+":"
            +str(int((tiempo_total%3600)%60)))

        '''

if __name__ == '__main__':
    main()