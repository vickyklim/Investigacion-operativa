import random

t = 20
o = 200 

tareas = [0]*3*o
i=0
id=0
while i<3*o:
    tareas[i] = id
    tareas[i+1] = random.randint(11000,32000) #beneficio
    tareas[i+2] = random.randint(3,12) #cant trabajadores
    id = id + 1
    i = i+3

c = 40 
conflictos = [0]*2*c
i=0
while i<2*c:
    conflictos[i], conflictos[i+1] = random.sample(range(t), 2)
    i = i+2

correl = 50 
correlativas = [0]*2*correl
i=0
while i<2*correl:
    correlativas[i], correlativas[i+1] = random.sample(range(o), 2)
    i = i+2

ord_conf = 185 
conflictivas = [0]*2*ord_conf
i=0
while i<2*ord_conf:
    conflictivas[i], conflictivas[i+1] = random.sample(range(o), 2)
    i = i+2

rep = 185
repetitivas = [0]*2*rep
i=0
while i<2*rep:
    repetitivas[i], repetitivas[i+1] = random.sample(range(o), 2)
    i = i+2


with open("nuestra_instancia.txt", "w") as file:
    file.write(f"{t}\n")
    file.write(f"{o}\n")
    for chunk_start in range(0, 3*o, 3):
        chunk = tareas[chunk_start:chunk_start + 3]
        file.write(f"{chunk[0]} {chunk[1]} {chunk[2]}\n")
    file.write(f"{c}\n")
    for chunk_start in range(0, 2*c, 2):
        chunk = conflictos[chunk_start:chunk_start + 2]
        file.write(f"{chunk[0]} {chunk[1]}\n")
    file.write(f"{correl}\n")
    for chunk_start in range(0, 2*correl, 2):
        chunk = correlativas[chunk_start:chunk_start + 2]
        file.write(f"{chunk[0]} {chunk[1]}\n")

    file.write(f"{ord_conf}\n")
    for chunk_start in range(0, 2*ord_conf, 2):
        chunk = conflictivas[chunk_start:chunk_start + 2]
        file.write(f"{chunk[0]} {chunk[1]}\n")
    file.write(f"{rep}\n")
    for chunk_start in range(0, 2*rep, 2):
        chunk = repetitivas[chunk_start:chunk_start + 2]
        file.write(f"{chunk[0]} {chunk[1]}\n")
