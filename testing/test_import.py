"""
Script de prueba para verificar la instalación
"""
from datetime import datetime
from astro_package import final_table as ft
from astro_package import moon_aptitude as mp

print("Probando importación de módulos...")
print("✓ final_table importado correctamente")
print("✓ moon_aptitude importado correctamente")

# Probar una funcionalidad básica
print("\nProbando funcionalidad básica...")

fecha = "28/07/2024 6:26"
latitud = "32s29"
longitud = "58w14"

# Convertir fecha
formato = '%d/%m/%Y %H:%M'
datetime_obj = datetime.strptime(fecha, formato)

# Crear instancia de moonAptitude
try:
    luna = mp.moonAptitude(datetime_obj, latitud, longitud)
    df = luna.generate_df()
    print("✓ Creación de instancia moonAptitude exitosa")
    print("✓ Generación de DataFrame exitosa")
    
    # Mostrar algunos resultados
    print("\nResultados de moonAptitude:")
    print(f"Puntos totales: {df.iloc[-2]['puntos']}")
    print(f"Porcentaje: {df.iloc[-1]['puntos']*100:.1f}%")
    
    print("\n✅ Instalación verificada correctamente!")
except Exception as e:
    print(f"\n❌ Error durante la prueba: {str(e)}")
