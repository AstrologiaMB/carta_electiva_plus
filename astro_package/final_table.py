import sys
import os
import pandas as pd
import numpy as np
import datetime as dt
#Mis librerias
#import settings_astro as st
from astro_package import moon_aptitude as mp 
from astro_package import rulership_asc as rasc
from astro_package import rulership_10 as r10
from astro_package import optimal_minutes as om
from astro_package import negative_minutes as nm
from astro_package import enraizar_a_bn as enr


class FinalTableGenerator:
    def __init__(self, dob_a, lat_a, lon_a, dob_bn, lat_bn, lon_bn,act="work"):
        self.dob_a = dob_a
        self.lat_a = lat_a
        self.lon_a = lon_a
        self.dob_bn = dob_bn
        self.lat_bn = lat_bn
        self.lon_bn = lon_bn
        self.act = act
        try:
            self.aptitud_luna = mp.moonAptitude(self.dob_bn,self.lat_bn,self.lon_bn,self.act).generate_df()
            self.regente_ascendente = rasc.rulershipConditions(self.dob_bn,self.lat_bn,self.lon_bn,self.act).merge_data()
            self.regente_casa_10 = r10.rulershipTen(self.dob_bn,self.lat_bn,self.lon_bn,self.act).merge_data()
            self.combinaciones_positivas = om.optimalMinutes(self.dob_bn,self.lat_bn,self.lon_bn,self.act).final_table()
            self.combinaciones_negativas = nm.negativeMinutes(self.dob_a,self.lat_a,self.lon_a,self.dob_bn,self.lat_bn,self.lon_bn,self.act).negative()
            self.enraizar_cartas = enr.enraizarCarta(self.dob_a,self.lat_a,self.lon_a,self.dob_bn,self.lat_bn,self.lon_bn,self.act).enraizar_carta()
            self.columna_puntaje = "puntos"
            self.columna_aptitud = "resultado"
        except Exception as e:
            raise ValueError(f"Error creating subject or natal: {str(e)}")
        
    #Para ver cuales estan Ok o No. Verdadero es no aptitud.
    def aptitud_logica(self,df):
                df_aptitud = df[df[self.columna_puntaje].isnull()]
                if df_aptitud.empty:
                    return np.nan
                df_aptitud.loc[:, 'resultado'] = df_aptitud['resultado'].apply(lambda x: True if x == 'True' or x==True else False)
                # Luego puedes verificar si hay algún valor True en la columna
                no_apta = df_aptitud[self.columna_aptitud].sum()>0
                return no_apta
    
    #Puntos Totales y en %
    def puntos(self,df):
                ptotal_puntos =df.iloc[-2]['puntos']
                total_puntos_porcentaje = round(df.iloc[-1]['puntos'],3)
                #max_puntos = ptotal_puntos/total_puntos_porcentaje
                #HARDCODEADO. CORREGIRRRRRRR
                max_puntos = 0
                return ptotal_puntos, total_puntos_porcentaje, max_puntos
    
    #Creo una fila de la tabla final
    def fila(self):
            # Código original comentado
            #score = (
            #    self.puntos(self.enraizar_cartas)[0] +
            #    self.puntos(self.aptitud_luna)[0] +
            #    self.puntos(self.regente_ascendente)[0] +
            #    self.puntos(self.regente_casa_10)[0] +
            #    self.puntos(self.combinaciones_positivas)[0] +
            #    self.puntos(self.combinaciones_negativas)[0]
            #        )
            #HARDCODEADO. CORREGIRRRRRRR
            #max_score = 37
            #max_score me interesa solo para la tabla final, que el máximo puede ser 14 el mínimo 6
            #puntos_tabla_enraizar, es el calculo de punto de la tabla enraizar
            #puntos_tabla_enraizar=self.puntos(self.enraizar_cartas)[0]
            #score=puntos_tabla_enraizar
            #max_score = 14 
            
            # Nuevo código: obtener porcentaje directamente de enraizar
            score_percentage = self.enraizar_cartas.iloc[-1]['puntos']
            
            # Mantener cálculo de color
            if score_percentage > 0.8:
                  color = 'Verde'
            elif score_percentage < 0.8 and score_percentage > 0.2:
                  color = 'Amarillo'
            else:
                  color = 'Rojo'
                  
            # Nueva estructura de fila con orden específico y formato consistente
            fila = {
                "Fecha": self.dob_bn.strftime("%Y-%m-%d %H:%M:%S"),
                "Puntaje total": f"{round(float(self.enraizar_cartas.iloc[-1]['puntos'])*100, 1)}%",
                "Color": color,
                "Sumatoria Rojos/Azules": f"{int(self.enraizar_cartas.iloc[-4, 4])}/{int(self.enraizar_cartas.iloc[-3, 4])}",
                "% Puntos Enraizar": f"{round(float(self.enraizar_cartas.iloc[-1]['puntos'])*100, 1)}%",
                "Luna": "Apta" if not self.aptitud_logica(self.aptitud_luna) else "No Apta",
                "% Puntos Luna": f"{round(float(self.aptitud_luna.iloc[-1]['puntos'])*100, 1)}%",
                "Regente ASC": "Apto" if not self.aptitud_logica(self.regente_ascendente) else "No Apto",
                "% Puntos Reg ASC": f"{round(float(self.regente_ascendente.iloc[-1]['puntos'])*100, 1)}%",
                "Regente 10": "Apto" if not self.aptitud_logica(self.regente_casa_10) else "No Apto",
                "% Puntos Reg 10": f"{round(float(self.regente_casa_10.iloc[-1]['puntos'])*100, 1)}%",
                "% Puntos Comb Pos": f"{round(float(self.combinaciones_positivas.iloc[-1]['puntos'])*100, 1)}%",
                "% Puntos Comb Neg": f"{round(float(self.combinaciones_negativas.iloc[-1]['puntos'])*100, 1)}%"
            }
            
            return fila, score_percentage
            
    
    

def generar_tabla(start_date, end_date, lat, lon, dob_bn, lat_bn, lon_bn, interval_hours = 3, score_threshold = 0):
    # Crea una lista para almacenar las filas
    filas = []
    
    # Itera sobre el rango de días
    current_moment = start_date
    while current_moment <= end_date:
        
        # Instanciar clase (dob_bn es carta A natal, current_moment es carta B(n))
        generador = FinalTableGenerator(dob_bn, lat_bn, lon_bn, current_moment, lat, lon)
        # Genera una fila
        fila, score_percentage = generador.fila()
        if score_percentage >= score_threshold:
            filas.append(fila)
        # Avanza de momento
        current_moment += dt.timedelta(hours=interval_hours)
    
    # Convierte la lista de filas en un DataFrame
    df_final = pd.DataFrame(filas)
    return df_final
