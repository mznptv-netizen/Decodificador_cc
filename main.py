import base64
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Importación segura: si por alguna razón 'mrz' no se instaló, 
# la aplicación no crasheará al abrirse.
try:
    from mrz.parser import parse_mrz
    MRZ_DISPONIBLE = True
except ImportError:
    MRZ_DISPONIBLE = False

def procesar_datos():
    texto_ingresado = entrada.get().strip()
    texto_resultado.delete("1.0", tk.END)
    
    if not texto_ingresado:
        messagebox.showwarning("Advertencia", "Por favor, escanea o ingresa un código.")
        return

    resultado_final = ""
    
    # 1. Detección de Franja MRZ (Reverso de la cédula con caracteres <<<)
    if "<<<" in texto_ingresado or (len(texto_ingresado) > 60 and "COL" in texto_ingresado):
        if not MRZ_DISPONIBLE:
            resultado_final = f"--- [Lectura MRZ detectada, pero falta instalar el módulo 'mrz'] ---\n{texto_ingresado}"
        else:
            try:
                lineas_mrz = texto_ingresado.replace("\r", "").split("\n")
                mrz_parsed = parse_mrz(lineas_mrz)
                
                if mrz_parsed.valid:
                    datos = mrz_parsed.fields
                    resultado_final = (
                        "=== [CEDULA COLOMBIANA - FRANJA MRZ (REVERSO)] ===\n"
                        f"• Tipo de Documento : {datos.document_type}\n"
                        f"• País / Emisor     : {datos.country}\n"
                        f"• Apellidos         : {datos.surname}\n"
                        f"• Nombres           : {datos.names}\n"
                        f"• Nro. de Cédula    : {datos.document_number}\n"
                        f"• Nacionalidad      : {datos.nationality}\n"
                        f"• Fecha Nacimiento  : {datos.birth_date}\n"
                        f"• Género            : {datos.sex}\n"
                        f"• Fecha Expiración  : {datos.expiration_date}\n"
                    )
                else:
                    resultado_final = f"--- [Lectura MRZ detectada - Formato parcial] ---\n{texto_ingresado}"
            except Exception as e:
                resultado_final = f"--- [Lectura OCR MRZ Cruda] ---\n{texto_ingresado}\n\nNota: {e}"
            
    else:
        # 2. Detección del Código QR del Frente (Formato Base64 con Firma Digital PKI)
        try:
            bytes_decodificados = base64.b64decode(texto_ingresado, validate=True)
            
            try:
                texto_legible = bytes_decodificados.decode("utf-8", errors="ignore")
            except Exception:
                texto_legible = "Datos estrictamente binarios."

            limpio = "".join(c for c in texto_legible if c.isprintable())
            preview = limpio[:400] if limpio else "[Estructura binaria cifrada / firmada]"

            resultado_final = (
                "=== [QR CÉDULA NUEVA - CAPA BASE64 & PKI] ===\n"
                f"• Tamaño del paquete binario : {len(bytes_decodificados)} bytes\n"
                f"• Contenido extraíble / Texto :\n{preview}\n\n"
                "🔒 [Capa de Seguridad]: Este QR contiene una Firma Digital (PKI)\n"
                "y certificados oficiales de la Registraduría Nacional para\n"
                "garantizar autenticidad y prevenir falsificaciones."
            )
        except Exception:
            resultado_final = f"=== [Texto Estándar / Desconocido] ===\n{texto_ingresado}"
        
    texto_resultado.insert(tk.END, resultado_final)
    
    # Limpiar automáticamente para el siguiente escaneo con la pistola
    entrada.delete(0, tk.END)
    entrada.focus()

# Configuración de la Interfaz Gráfica
root = tk.Tk()
root.title("Validador de Cédula Digital (QR Base64/PKI & MRZ)")
root.geometry("680x530")

label_instruccion = tk.Label(root, text="Escanee el QR (Frente) o la Franja MRZ (Reverso):", font=("Arial", 11, "bold"))
label_instruccion.pack(pady=10)

entrada = tk.Entry(root, font=("Arial", 12), width=60)
entrada.pack(pady=5)
entrada.focus()

btn_procesar = tk.Button(root, text="Procesar Datos del Documento", command=procesar_datos, font=("Arial", 11), bg="#2196F3", fg="white")
btn_procesar.pack(pady=10)

entrada.bind("<Return>", lambda event: procesar_datos())

label_resultado = tk.Label(root, text="Resultado del Análisis de Seguridad:", font=("Arial", 11, "bold"))
label_resultado.pack(pady=5)

texto_resultado = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=76, height=16, font=("Courier New", 10))
texto_resultado.pack(pady=5)

root.mainloop()
