import base64
import sys

def decodificar_datos(datos_base64, archivo_salida):
    try:
        # Convertir la cadena Base64 a bytes
        datos_decodificados = base64.b64decode(datos_base64)
        
        # Guardar en el archivo especificado
        with open(archivo_salida, "wb") as f:
            f.write(datos_decodificados)
            
        print(f"Decodificación exitosa. Archivo guardado como: {archivo_salida}")
    except Exception as e:
        print(f"Error al decodificar: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python main.py <cadena_base64> <archivo_salida>")
    else:
        cadena = sys.argv[1]
        salida = sys.argv[2]
        decodificar_datos(cadena, salida)
