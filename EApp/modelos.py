from math import exp, pi, pow, log
from scipy.optimize import fsolve
import numpy as np


def densidad_aire(Tam, Hr):
    """Densidad del aire.
    
    Calcula la densidad del aire húmedo en unidades de kg/m3, como función de la temperatura y la humedad relativa
    a una 1 atmosfera de presión.

    Parámetros:
    Tam: Temperatura del ambiente en unidades de grados Celsius (°C).
    Hr: Humedad relativa del ambiente expresada en porcentaje (%).

    """
    # :::::::::::::::: Se definen constantes del aire y vapor de agua
    Ma=18.015          # Pesos Molecular Agua (kg/kmol)
    Mb=28.965          # Pesos Molecular Aire (kg/kmol)
    A=23.7093          # Constantes de la ecuacion de Antoine para presion de vapor
    B=4111
    C=237.7
    R=8.3145           # Constante universal de los gases (kPa*m3/kmol*k)
    P=101.325          # Presion atmosferica (kPa)

    Hr=Hr/100
    T=273.15+Tam                   # Temperatura en kelvin
    Ps=(exp(A-B/(C+Tam)))/1000     # Presion de vapor (kPa)
    Pa=Hr*Ps                       # Presion parcial del vapor (kPa)
    Y=(Ma/Mb)*(Pa/(P-Pa))          # Humedad absoluta (kg agua/kg aire)
    VH=(1/Mb+Y/Ma)*((R*T)/P)       # Volumen humedo (m3/kg gas)
    da=1/VH                        # Densidad del aire humedo (kg/m3)
    return da


def potencia_viento(Vel, Tam, Hr): 
    """Potencia de aerogenerador.

    Calcula la potencia del aerogenerador en unidades de vatios (W), como una función de la velocidad 
    del viento, la temperatura y la humedad relativa.

    Parámetros:
    Vel: Velocidad del viento en unidades de metro por segundo (m/s).
    Tam: Temperatura del ambiente en unidades de grados Celsius (°C).
    Hr: Humedad relativa del ambiente expresada en porcentaje (%).

    """
    # :::::::::::::::::::::::: Parametros del aerogenerador
    r=5                        # Longitud de la pala (m)
    beta=0                     # Ángulo de ataque
    RPM=16                     # Velocidad rotacional del aerogenerador
    ohm=r*RPM*0.10472          # Velocidad rotacional del aerogenerador 16 rpm    

    da=densidad_aire(Tam, Hr)    # Densidad del aire (kg/m3)
    lamb=ohm*r/Vel               
    invdelta=(1/lamb)-0.035      
    CP=0.5*((116*invdelta)-5)*exp(-21*invdelta)
    P=(1/2)*da*CP*pi*(pow(r,2))*(pow(Vel,3))
    return P


def potencia_viento_modificada(Vel, Tam, Hr):
    """Potencia de aerogenerador modificada.

    Calcula la potencia del aerogenerador en unidades de vatios (W), se tiene en cuenta la modificación que 
    a velocidades superiores a la velocidad óptima de operación del aerogenerador, la potencia de salida será 
    igual a la potencia máxima.

    Parámetros:
    Vel: Velocidad del viento en unidades de metro por segundo (m/s).
    Tam: Temperatura del ambiente en unidades de grados Celsius (°C).
    Hr: Humedad relativa del ambiente expresada en porcentaje (%).

    """
    # Simulacion de velocidades
    Vel_list=[x for x in np.linspace(1,20,190)]
    P_list=list()
    for v in Vel_list:
        p=potencia_viento(v,Tam,Hr)
        P_list.append(p)

    P_max=max(P_list)                 # Potencia Máxima Generada
    P_index=P_list.index(P_max)       # Indice de la potencia máxima
    Vel_opt=Vel_list[P_index]         # Velocidad Óptima
    if(Vel >= Vel_opt):
        pot=P_max
    else:
        pot=potencia_viento(Vel,Tam,Hr)
    return pot


def potencia_solar(ToC, Go, V):
    """Potencia generada por el Panel Solar.

    Potencia generada por el Panel Solar en unidades de vatios (W), como función de la temperatura, 
    la Irradiancia solar y el Voltaje de operación del panel.

    Parámetros:
    ToC: Temperatura del ambiente en unidades de grados Celsius (°C).
    Go: Irradiancia solar DHI en unidades de vatios por metro cuadrado (W/m2). 
    V: Voltaje de operación del panel en uniadades de voltios (V).

    """
    # ::::::::::::::::Constantes
    K=1.38e-23     # Constante de Boltzman
    q=1.602e-19    # Carga del electrón
    Eg=1.12        # Banda de separación del silicio at 23 grados
    # ::::::::::::::::Valores de hoja de datos
    Isc=3.87       # Corriente de corto nominal
    Impp=3.52      # Corriente nominal
    Voc=42.1       # Voltaje de circuito abierto nominal
    Vmpp=33.7      # Voltaje nominal        
    Kv=-0.160      # Coeficiente de temperatura del voltaje de circuito abierto
    Ki=0.065       # Coeficiente de temperatura de la corriente de corto
    Ns=72         # Número de celdas en series  <-----MODELO PANEL MSX120
    Pmpp=Impp*Vmpp # Potencia nominal = 118.624 W  

    # ::::::::::::: Valores de operación estándar STC
    Tn=25+273      # Temperatura nominal 
    Gn=1000        # Irradiancia nominal
    Rsh=924824.733    # Resistencia shunt  <----------SOLUCION DE SISTEMA DE ECUACIONES
    Rs=0.284       # Resistencia serie
    Vt=0.019       # Voltaje término en condiciones estándar (STC)
    A=0.738        # Factor de calidad del diodo 

    To=ToC+273     # Temperatura de operación en kelvin

    # A) Ajuste de temperatura en Voltaje término
    Vt_To=Vt*To/Tn
    #Vt_To=Vt

    # B) Expresión para corriente fotogenerada Iph y corriente de saturación oscura Io a condiciones estándar 
    Io_stc=(Isc-((Voc-Isc*Rs)/Rsh))*exp(-Voc/(Ns*Vt))
    Iph_stc=Io_stc*exp((Voc/(Ns*Vt)))+(Voc/Rsh)

    # C) Dependencia de la irradiancia de la corriente de corto circuito y de la corriente foto generada
    Isc_G=Isc*Go/Gn
    Iph_G=Iph_stc*Go/Gn

    # E) Dependencia de la temperatura de la corriente de corto circuito
    Isc_GT=Isc_G*(1+((Ki/100)*(To-Tn)))

    # D) Dependencia de la irradiancia del voltaje de circuito abierto
    #Voc_T=Voc+(Kv*(To-Tn))
    def f_VocG(xx):
        return (log((Iph_G*Rsh-xx)/(Io_stc*Rsh))*Ns*Vt_To)-xx
    root = fsolve(f_VocG, Voc)
    Voc_G=root[0]
    Voc_GT=Voc_G+(Kv*(To-Tn))

    # G) Dependencia de irradiancia y temperatura en la corriente de saturación oscura 
    Io_GT=(Isc_GT-((Voc_GT-Isc_GT*Rs)/Rsh))*exp(-Voc_GT/(Ns*Vt_To))

    # H) Dependencia de la temperatura de la corriente fotogenerada
    Iph_GT=Io_GT*exp((Voc_GT/(Ns*Vt_To)))+(Voc_GT/Rsh)

    def f_Ipv(xxx):
        return Iph_GT-xxx-((V+Rs*xxx)/Rsh)-(Io_GT*((exp((V+xxx*Rs)/(Ns*Vt_To)))-1))
    root2 = fsolve(f_Ipv, 3.52)
    Ipv=root2[0]

    if Ipv > 0:
        P=V*Ipv
    else:
        P=0
    return P