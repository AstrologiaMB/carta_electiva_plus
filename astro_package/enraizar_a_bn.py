# standard
import json
from datetime import datetime
import csv
import sys
import os
# third party
from immanuel import charts
from immanuel.const import chart, dignities
from immanuel.classes.serialize import ToJSON
from immanuel.setup import settings
import pandas as pd
import numpy as np
from immanuel import charts
from immanuel.const import calc,chart, dignities
from immanuel.classes.serialize import ToJSON
from immanuel.setup import settings
import pandas as pd
import numpy as np
import csv


# yours
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from astro_package.settings_astro import *

class enraizarCarta:
    def __init__(self, dob_a, lat_a, lon_a, dob_bn, lat_bn, lon_bn,act="work"):
        self.dob_a = dob_a
        self.lat_a = lat_a
        self.lon_a = lon_a
        self.dob_bn = dob_bn
        self.lat_bn = lat_bn
        self.lon_bn = lon_bn
        self.act = act

        try:
            # carta A (natal)
            self.subject_a = charts.Subject(dob_a, lat_a, lon_a)  # Datos natales
            self.natal_a = charts.Natal(self.subject_a)  # Carta natal
            self.aspects_json_a = json.dumps(self.natal_a.aspects, cls=ToJSON, indent=4)
            self.aspect_json_a = json.loads(self.aspects_json_a)
            self.objects_json_a = json.dumps(self.natal_a.objects, cls=ToJSON, indent=4)
            self.object_json_a = json.loads(self.objects_json_a)
            self.asc_sign_a = self.natal_a.objects[chart.ASC].sign.number
            self.asc_ruler_a = str(dignities.TRADITIONAL_RULERSHIPS[self.asc_sign_a])
            self.house_10_sign_a = self.natal_a.houses[chart.HOUSE10].sign.number
            self.r10=str(dignities.TRADITIONAL_RULERSHIPS[self.house_10_sign_a])

            # carta B(n) (momento)
            self.subject_bn = charts.Subject(dob_bn, lat_bn, lon_bn)  # Datos del momento
            self.natal_bn = charts.Natal(self.subject_bn)  # Carta del momento
            self.aspects_json_bn = json.dumps(self.natal_bn.aspects, cls=ToJSON, indent=4)
            self.aspect_json_bn = json.loads(self.aspects_json_bn)
            self.objects_json_bn = json.dumps(self.natal_bn.objects, cls=ToJSON, indent=4)
            self.object_json_bn = json.loads(self.objects_json_bn)
            self.asc_sign_bn = self.natal_bn.objects[chart.ASC].sign.number
            self.asc_ruler_bn = str(dignities.TRADITIONAL_RULERSHIPS[self.asc_sign_bn])
            self.house_10_sign_bn = self.natal_bn.houses[chart.HOUSE10].sign.number
            self.r10=str(dignities.TRADITIONAL_RULERSHIPS[self.house_10_sign_bn])

        except Exception as e:
            raise ValueError(f"Error creating subject or natal: {str(e)}")

    @staticmethod
    def dgs_to_dcl(degrees, minutes, seconds):
        dd = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
        return dd

    @staticmethod
    def calculate_percentage(points, total_conditions):
        return (points / (total_conditions * 2)) * 100

    def get_house_degrees(self, house_info):
        # angulo de inicio de la casa
        house_start_degree = house_info['lon']
        # tamaño de la casa
        house_size = house_info['size']
        house_end_degree = (house_start_degree + house_size) % 360

        return house_start_degree, house_end_degree

    @staticmethod
    def aspect(degree1, degree2, grado, orb = None):
        if orb is None:
            orb = settings.planet_orbs[grado]
        # Convertir a float para mantener decimales
        degree1 = float(degree1)
        degree2 = float(degree2)
        # Calcular diferencia manteniendo decimales
        diferencia = abs(degree1 - degree2) % 360
        diferencia = min(diferencia, 360-diferencia)
        # Verificar si está dentro del orbe del aspecto
        return abs(diferencia - grado) <= orb

    def enraizar_carta(self):
        tabla = []
        total_points = 0
        orb = 5

        # Obtener posiciones de la carta natal (A)
        asc_natal = self.natal_a.objects[chart.ASC].longitude.raw
        sat_natal = self.natal_a.objects[chart.SATURN].longitude.raw
        marte_natal = self.natal_a.objects[chart.MARS].longitude.raw
        jup_natal = self.natal_a.objects[chart.JUPITER].longitude.raw
        sol_natal = self.natal_a.objects[chart.SUN].longitude.raw
        luna_natal = self.natal_a.objects[chart.MOON].longitude.raw
        ven_natal = self.natal_a.objects[chart.VENUS].longitude.raw

        # Obtener posiciones de la carta del momento (B(n))
        asc_moment = self.natal_bn.objects[chart.ASC].longitude.raw
        # Aspectos
        conjuncion = 0.0
        trigono = 120.0
        sextil = 60.0
        # Colores
        azul = "Azul"
        rojo = "Rojo"
        vacio = "Ninguno"
        # Condición 1: Si el ASC de la carta B(n) coincide con el grado de Saturno de la carta natal A
        resultado = self.aspect(asc_moment, sat_natal, conjuncion, orb)
        color= rojo if resultado else vacio
        punto= -2 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append(
            {
                "cond_num": 1,
                "Condicion": "Si el ASC de la carta B(n) coincide con el grado de Saturno de la carta natal A (usar orbe 5 o menos)",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Condición 2: ASC de la carta B(n) coincide con el grado de Marte de la carta natal A
        resultado = self.aspect(asc_moment, marte_natal, conjuncion, orb)
        color = rojo if resultado else vacio
        punto = -2 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append(
            {
                "cond_num": 2,
                "Condicion": "ASC de la carta B(n) coincide con el grado de Marte de la carta natal A (usar orbe 5 o menos)",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Condición 3: ASC de la carta B(n) está en la casa 6 de la carta natal A
        house_info_6 = self.natal_a._houses[chart.HOUSE6]  # Casas de la carta natal
        house_start_degree, house_end_degree = self.get_house_degrees(house_info_6)
        resultado = (house_start_degree <= asc_moment <= house_end_degree)
        color = rojo if resultado else vacio
        punto = -2 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append(
            {
                "cond_num": 3,
                "Condicion": "ASC de la carta B(n) está en la casa 6 de la carta natal A",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Condición 4: ASC de la carta B(n) está en la casa 8 o 12 de la carta natal A
        house_info_8 = self.natal_a._houses[chart.HOUSE8]  # Casas de la carta natal
        house_info_12 = self.natal_a._houses[chart.HOUSE12]  # Casas de la carta natal
        house_start_degree_8, house_end_degree_8 = self.get_house_degrees(house_info_8)
        house_start_degree_12, house_end_degree_12 = self.get_house_degrees(house_info_12)
        house_8 = (house_start_degree_8 <= asc_moment <= house_end_degree_8)
        house_12 = (house_start_degree_12 <= asc_moment <= house_end_degree_12)
        resultado= house_8 or house_12
        color= np.nan
        punto= -2 if resultado else 0
        tabla.append(
            {
                "cond_num": 4,
                "Condicion": "ASC de la carta B(n) está en la casa 8 o 12 de la carta natal A",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Condición 5: ASC de la carta B(n) está conjunto al ASC de la carta natal A
        resultado = self.aspect(asc_moment, asc_natal, conjuncion, orb)
        color = azul if resultado else vacio
        punto = 2 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append(
            {
                "cond_num": 5,
                "Condicion": "ASC de la carta B(n) está conjunto al ASC de la carta natal A",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Condición 6: ASC de la carta B(n) está en trígono al ASC de la carta natal A
        resultado = self.aspect(asc_moment, asc_natal, trigono, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append(
            {
                "cond_num": 6,
                "Condicion": "ASC de la carta B(n) está en trígono al ASC de la carta natal A",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Condición 7: ASC de la carta B(n) está en sextil al ASC de la carta natal A
        resultado = self.aspect(asc_moment, asc_natal, sextil, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append(
            {
                "cond_num": 7,
                "Condicion": "ASC de la carta B(n) está en sextil al ASC de la carta natal A",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Condición 8: ASC de la carta B(n) está conjunto al Sol de la carta natal A
        resultado = self.aspect(asc_moment, sol_natal, conjuncion, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append(
            {
                "cond_num": 8,
                "Condicion": "ASC de la carta B(n) está conjunto al Sol de la carta natal A",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Condición 9: ASC de la carta B(n) está en trígono al Sol de la carta natal A
        resultado = self.aspect(asc_moment, sol_natal, trigono, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append(
            {
                "cond_num": 9,
                "Condicion": "ASC de la carta B(n) está en trígono al Sol de la carta natal A",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Condición 10: ASC de la carta B(n) está en sextil al Sol de la carta natal A
        resultado = self.aspect(asc_moment, sol_natal, sextil, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append(
            {
                "cond_num": 10,
                "Condicion": "Si el ASC de la carta B(n) esta sextil al Sol de la carta natal natal A (usar orbe)",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Condición 11: ASC de la carta B(n) está conjunto a la Luna de la carta natal A
        resultado = self.aspect(asc_moment, luna_natal, conjuncion, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append({
            "cond_num": 11,
            "Condicion": "ASC de la carta B(n) está conjunto a la Luna de la carta natal A",
            "Resultado": resultado,
            "Color": color,
            "Punto": punto
        })

        # Condición 12: ASC de la carta B(n) está en trígono a la Luna de la carta natal A
        resultado = self.aspect(asc_moment, luna_natal, trigono, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append({
            "cond_num": 12,
            "Condicion": "ASC de la carta B(n) está en trígono a la Luna de la carta natal A",
            "Resultado": resultado,
            "Color": color,
            "Punto": punto
        })

        # Condición 13: ASC de la carta B(n) está en sextil a la Luna de la carta natal A
        resultado = self.aspect(asc_moment, luna_natal, sextil, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append({"cond_num":13, 
                      "Condicion":"Si el ASC de la carta B(n) esta sextil a la Luna  de la carta natal natal A (usar orbe)", 
                      "Resultado": resultado, 
                      "Color": color, 
                      "Punto": punto})

        # Condición 14: ASC de la carta B(n) está conjunto a Venus de la carta natal A
        resultado = self.aspect(asc_moment, ven_natal, conjuncion, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append({
            "cond_num": 14,
            "Condicion": "ASC de la carta B(n) está conjunto a Venus de la carta natal A",
            "Resultado": resultado,
            "Color": color,
            "Punto": punto
        })

        # Condición 15: ASC de la carta B(n) está en trígono a Venus de la carta natal A
        resultado = self.aspect(asc_moment, ven_natal, trigono, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append({
            "cond_num": 15,
            "Condicion": "ASC de la carta B(n) está en trígono a Venus de la carta natal A",
            "Resultado": resultado,
            "Color": color,
            "Punto": punto
        })

        # Condición 16: ASC de la carta B(n) está en sextil a Venus de la carta natal A
        resultado = self.aspect(asc_moment, ven_natal, sextil, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append({
            "cond_num": 16,
            "Condicion": "ASC de la carta B(n) está en sextil a Venus de la carta natal A",
            "Resultado": resultado,
            "Color": color,
            "Punto": punto
        })

        # Condición 17: ASC de la carta B(n) está conjunto a Júpiter de la carta natal A
        resultado = self.aspect(asc_moment, jup_natal, conjuncion, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append({
            "cond_num": 17,
            "Condicion": "ASC de la carta B(n) está conjunto a Júpiter de la carta natal A",
            "Resultado": resultado,
            "Color": color,
            "Punto": punto
        })

        # Condición 18: ASC de la carta B(n) está en trígono a Júpiter de la carta natal A
        resultado = self.aspect(asc_moment, jup_natal, trigono, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append({
            "cond_num": 18,
            "Condicion": "ASC de la carta B(n) está en trígono a Júpiter de la carta natal A",
            "Resultado": resultado,
            "Color": color,
            "Punto": punto
        })

        # Condición 19: ASC de la carta B(n) está en sextil a Júpiter de la carta natal A
        resultado = self.aspect(asc_moment, jup_natal, sextil, orb)
        color = azul if resultado else vacio
        punto = 1 if resultado else 0
        total_points += punto if resultado else 0
        tabla.append(
            {
                "cond_num": 19,
                "Condicion": "Si el ASC de la carta B(n) esta en sextil a Jupiter de la carta natal natal A (usar orbe)",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Condición 20: Cúspide de la casa 10 del momento está conjunta a Júpiter natal
        house_info_10 = self.natal_bn._houses[chart.HOUSE10]  # Casa 10 de la carta del momento
        house_10_cusp, _ = self.get_house_degrees(house_info_10)
        resultado = self.aspect(house_10_cusp, jup_natal, conjuncion, orb)
        color = azul if resultado else vacio
        punto = 2 if resultado else 0
        tabla.append({
            "cond_num": 20,
            "Condicion": "Cúspide de la casa 10 del momento está conjunta a Júpiter natal",
            "Resultado": resultado,
            "Color": color,
            "Punto": punto
        })

        # Condición 21: Cúspide de la casa 10 del momento está conjunta a Venus natal
        resultado = self.aspect(house_10_cusp, ven_natal, conjuncion, orb)
        color = azul if resultado else vacio
        punto = 2 if resultado else 0
        tabla.append({
            "cond_num": 21,
            "Condicion": "Cúspide de la casa 10 del momento está conjunta a Venus natal",
            "Resultado": resultado,
            "Color": color,
            "Punto": punto
        })

        # Condición 22: Cúspide de la casa 10 del momento está conjunta al Sol natal
        resultado = self.aspect(house_10_cusp, sol_natal, conjuncion, orb)
        color = azul if resultado else vacio
        punto = 2 if resultado else 0
        tabla.append({
            "cond_num": 22,
            "Condicion": "Cúspide de la casa 10 del momento está conjunta al Sol natal",
            "Resultado": resultado,
            "Color": color,
            "Punto": punto
        })

        # Condición 23: Cúspide de la casa 10 del momento está conjunta a la Luna natal
        resultado = self.aspect(house_10_cusp, luna_natal, conjuncion, orb)
        color = azul if resultado else vacio
        punto = 2 if resultado else 0
        tabla.append(
            {
                "cond_num": 23,
                "Condicion": "Si la cuspide de la casa 10 de la carta B(n) esta conjunto a la Luna de la carta A (usar orbe)",
                "Resultado": resultado,
                "Color": color,
                "Punto": punto,
            }
        )

        # Contar cantidad de condiciones y puntos
        cant_rojos = sum(1 for item in tabla if item['Color'] == rojo)
        cant_azules = sum(1 for item in tabla if item['Color'] == azul)
        puntos_rojos = sum(item['Punto'] for item in tabla if item['Color'] == rojo)
        puntos_azules = sum(item['Punto'] for item in tabla if item['Color'] == azul)

        # Agregar detalles de puntuación
        tabla.append(
            {
                "cond_num": None,
                "Condicion": "Cantidad Condiciones Rojas",
                "Resultado": f"{cant_rojos} condiciones = {puntos_rojos} puntos",
                "Color": rojo,
                "Punto": cant_rojos,
            }
        )
        tabla.append(
            {
                "cond_num": None,
                "Condicion": "Cantidad Condiciones Azules",
                "Resultado": f"{cant_azules} condiciones = {puntos_azules} puntos",
                "Color": azul,
                "Punto": cant_azules,
            }
        )

        # Agregar total de puntos
        tabla.append(
            {
                "cond_num": None,
                "Condicion": "Total Puntos",
                "Resultado": f"Rojos({puntos_rojos}) + Azules({puntos_azules}) = {total_points}",
                "Color": "",
                "Punto": total_points,
            }
        )

        # Calcular porcentaje
        max_puntos = 14.0  # Máximo teórico: 9 puntos azules + 5 puntos de margen
        porcentaje = total_points / max_puntos
        
        tabla.append(
            {
                "cond_num": None,
                "Condicion": "Total Puntos %",
                "Resultado": f"{total_points} / {max_puntos} = {porcentaje * 100:.1f}%",
                "Color": "",
                "Punto": porcentaje,
            }
        )
        df = pd.DataFrame(tabla)
        df.rename(columns={ "Resultado": "resultado", "Punto":"puntos"}, inplace=True)

        return df
