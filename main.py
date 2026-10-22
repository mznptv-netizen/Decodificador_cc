import base64
import tkinter as tk
from tkinter import messagebox, scrolledtext

def decodificar():
    texto_ingresado = entrada.get().strip()
    texto_resultado.delete("1.0", tk.END)
    
    if not texto_ingresado:
        messagebox.showwarning("Advertencia", "Por favor, escanea o ingresa un texto.")
        return

    resultado_final = ""
    
    # 1. Verificar si es una franja MRZ (identificada por las flechas '<<<')
    if "<<<" in texto_ingresado:
        resultado_final = f"--- [Detectado MRZ / OCR Honeywell] ---\n{texto_ingresado}"
        
    else:
        # 2. Intentar decodificar como Base64 (para códigos QR)
        try:
            bytes_decodificados = base64.b64decode(texto_ingresado, validate=True)
            try:
                texto_decodificado = bytes_decodificados.decode("utf-8")
                resultado_final = f"--- [Detectado como Base64 (QR)] ---\n{texto_decodificado}"
            except UnicodeDecodeError:
                resultado_final = f"--- [Base64 a Hexadecimal] ---\n{bytes_decodificados.hex()}"
        except Exception:
            # 3. Si no es Base64 ni MRZ, se muestra como texto plano
            resultado_final = f"--- [Texto Plano / Estándar] ---\n{texto_ingresado}"
        
    texto_resultado.insert(tk.END, resultado_final)
    
    # Limpiar automáticamente la entrada para el siguiente escaneo rápido
    entrada.delete(0, tk.END)
    entrada.focus()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Lector Universal: QR (Base64) & MRZ (OCR)")
root.geometry("600x450")

label_instruccion = tk.Label(root, text="Escanea el Código QR (Base64) o la Franja MRZ (OCR):", font=("Arial", 11, "bold"))
label_instruccion.pack(pady=10)

# Campo donde el escáner (QR o Honeywell OCR) escribe automáticamente
entrada = tk.Entry(root, font=("Arial", 12), width=50)
entrada.pack(pady=5)
entrada.focus()

btn_procesar = tk.Button(root, text="Procesar Datos", command=decodificar, font=("Arial", 11), bg="#2196F3", fg="white")
btn_procesar.pack(pady=10)

# Al presionar Enter (automático por el escáner), procesa al instante
entrada.bind("<Return>", lambda event: decodificar())

label_resultado = tk.Label(root, text="Resultado de la Lectura:", font=("Arial", 11, "bold"))
label_resultado.pack(pady=5)

# Área de texto para ver el resultado detallado
texto_resultado = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=68, height=12, font=("Arial", 10))
texto_resultado.pack(pady=5)

root.mainloop()
# Área de texto donde se muestra el resultado
texto_resultado = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=55, height=10, font=("Arial", 10))
texto_resultado.pack(pady=5)

root.mainloop()
