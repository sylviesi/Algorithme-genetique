import math
import random
import time

temps = time.process_time()

print("entrer la taille de la population")
popsize = int(input())
print("entrer le profil 1,2 ou 3")
profil=int(input())
print("entrer le nb d'itérations")
nb_ite=int(input())
A = 1000
Cp = 100
hr = 0.1
P = []
T = []
B = []
TP = []
wselect = []  # liste qui retiens les individus sélectionnés par la méthode de la roulette
listecross = [] # liste qui retiens les individus qui sont sélectionnés pour le croisement
'''On déclare et on initialise les variables globales qui vont servir dans le reste de l'algo'''

def calc_TP (p,t,b):
    global A,hr,Cp,profil
    phi = 30 * (1 - math.exp(-b / 1195))
    D = demande(profil,p)
    Q = t * D
    tp = ((p + phi) * D - (A * D / Q) - (Cp * D) - (hr * Cp * Q * 0.5) - b)
    return (tp)
'''C'est la fonction qui sert à calculer la valeur de la fitness fonction selon les variables d'entrée'''

def demande (profil,p):

    if profil==1:
        D = -0.003539 * p ** 3 + 2.1215 * p ** 2 - 413.3 * p + 26580
        return (D)
    elif profil==2:
        D = -0.002703 * p ** 3 + 1.577 * p ** 2 - 296.8 * p + 18413
        return (D)
    else:
        D = -0.0023 * p ** 3 + 1.35 * p ** 2 - 254.5 * p + 15500
        return (D)
'''Fonction qui sert à  calculer la demande selon le profil sélectionné pour l'utilisateur'''

def inititialisation ():
    global A, Cp, hr,total2,P,best,besti
    best = 0
    besti = 0
    TP[:] = []
    P[:] = []
    T[:] = []
    B[:] = []
    for i in range(popsize):
        tpm=-1
        while tpm < 0:
            pi = random.uniform(170, 270)
            ti = random.random()
            bi = random.uniform(0, 15000)
            tpm=calc_TP(pi,ti,bi)
        P.append(pi)
        T.append(ti)
        B.append(bi)
        TP.append(tpm)
'''Dans cette fontion d'initialisation, on génère une population de façon "aléatoire" en respectant les contraintes
   imposées dans l'article. On interdit également des valeurs nules pour la fitness fonction. '''

def methode_roulette ():
    global total2,P,wselect
    wselect[:]=[]
    for i in range(len(P)):
        roulette = random.random()
        j = 1
        total_TP=sum(TP)
        calc = TP[0] / total_TP
        while calc < roulette:
            calc = calc + TP[j] / total_TP
            j = j + 1
        wselect.append(j - 1)
    wselect = list(set(wselect))
'''Cette fonction permet de sélectionner des individus selon la méthode de la roulette. On obtiens au final la liste 
    des individus sélectionnés par la méthode de la roulette et ils servirons pour la prochaine étape (croisement).'''

def croisement ():
    global P,T,B,TP,listecross
    listecross[:] = []
    if len(wselect) > 1:
        for i in range(len(wselect)):
            if random.randint(1, 10) < 3:
                listecross.append(i)

        if len(listecross) % 2 != 0:
            bool = 0
            while bool != 1:
                chos = random.randint(0, len(wselect) - 1)
                if chos not in listecross:
                    listecross.append(chos)
                    bool = 1
        i = 0
        '''On croise les individus sélectionnées par la méthode de la roulette avec un taux de croisement de 0,2
        et on fait en sorte de sélectionner un nombre pair d'individus'''

        while i < len(listecross):
            crosspoint = random.randint(1, 2)
            if crosspoint != 1:
                a1 = listecross[i]
                a2 = listecross[i + 1]
                P.append(P[a1])
                T.append(T[a1])
                B.append(B[a2])
                P.append(P[a2])
                T.append(T[a2])
                B.append(B[a1])
                TP.append(calc_TP(P[a1], T[a1], B[a2]))
                TP.append(calc_TP(P[a2], T[a2], B[a1]))
            else:
                a1 = listecross[i]
                a2 = listecross[i + 1]
                P.append(P[a1])
                T.append(T[a2])
                B.append(B[a2])
                P.append(P[a2])
                T.append(T[a1])
                B.append(B[a1])
                TP.append(calc_TP(P[a1], T[a2], B[a2]))
                TP.append(calc_TP(P[a2], T[a1], B[a1]))
            i = i + 2
            '''On réalise de croisement des individus avec un seul point de croisement '''

def mutation ():
    global P,T,B,TP,popsize
    for i in range(len(listecross)):
        if random.randint(1, 10) < 2:
            TP[popsize+i] = -1
            while TP[popsize+i] < 0:
                P[popsize + i] = random.uniform(100, 270)
                T[popsize + i] = random.random()
                B[popsize + i] = random.uniform(0, 15000)
                TP[popsize + i] = calc_TP(P[popsize + i],T[popsize + i],B[popsize + i])
'''On fait muter les individus inssus du croisement avec un taux de mutation de 0,1 en intersant toujours 
les valeurs négatives pour TP'''

def selection ():
    global P,B,T,best,besti, index
    B2=[]
    T2=[]
    P2=[]
    TP2=[]
    TP2[:]=TP[:]
    B2[:]=B[:]
    T2[:]=T[:]
    P2[:]=P[:]
    B[:] = []
    T[:] = []
    P[:] = []
    TP[:] = []
    dist=len(TP2)
    for i in range (dist):
        indice=TP2.index(max(TP2))
        TP.append(TP2[indice])
        B.append(B2[indice])
        T.append(T2[indice])
        P.append(P2[indice])
        del TP2[indice]
        del B2[indice]
        del T2[indice]
        del P2[indice]
    del B[popsize:]
    del T[popsize:]
    del P[popsize:]
    del TP[popsize:]
    if TP[0] > best:
        best = TP[0]
        besti = index
'''On sélectionne les 100 meilleurs individus parmis les 100 parents et les enfants issus des croisements et de la 
   mutation.'''


result=[]
result2=[]
for x in range (nb_ite): #pour faire x fois l'algo
    test=inititialisation()
    for index in range(100):  # on répète l'expérience 100 fois
        test2=methode_roulette()
        test3=croisement()
        test4=mutation()
        test5=selection()
    result.append(best)
    result2.append(besti)

print("moyenne Tp",sum(result) / nb_ite)
print("besti=",sum(result2)/nb_ite)
print("tps de calc",time.process_time() - temps)
