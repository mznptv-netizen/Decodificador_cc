import base64
import tkinter as tk
from tkinter import messagebox, scrolledtext

def decodificar():
    texto_base64 = entrada.get().strip()
    texto_resultado.delete("1.0", tk.END)
    
    if not texto_base64:
        messagebox.showwarning("Advertencia", "Por favor, escanea o ingresa un código.")
        return

    try:
        # Decodificar de Base64
        bytes_decodificados = base64.b64decode(texto_base64)
        try:
            # Intentar convertir a texto legible (UTF-8)
            resultado = bytes_decodificados.decode("utf-8")
        except UnicodeDecodeError:
            resultado = str(bytes_decodificados)
            
        texto_resultado.insert(tk.END, resultado)
    except Exception as e:
        texto_resultado.insert(tk.END, f"Error al decodificar: {e}")

# Configuración de la ventana gráfica
root = tk.Tk()
root.title("Decodificador de Escáner")
root.geometry("500x400")

label_instruccion = tk.Label(root, text="Escanea o ingresa los datos aquí:", font=("Arial", 11))
label_instruccion.pack(pady=10)

# Campo de entrada (aquí escribirá automáticamente tu lector/escáner)
entrada = tk.Entry(root, font=("Arial", 12), width=40)
entrada.pack(pady=5)
entrada.focus()  # Mantiene el cursor listo para recibir el escaneo

# Botón para decodificar manualmente
btn_decodificar = tk.Button(root, text="Decodificar", command=decodificar, font=("Arial", 11), bg="#4CAF50", fg="white")
btn_decodificar.pack(pady=10)

# Permitir presionar la tecla Enter para decodificar automáticamente
entrada.bind("<Return>", lambda event: decodificar())

label_resultado = tk.Label(root, text="Resultado decodificado:", font=("Arial", 11))
label_resultado.pack(pady=5)

# Área de texto donde se muestra el resultado
texto_resultado = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=55, height=10, font=("Arial", 10))
texto_resultado.pack(pady=5)

root.mainloop()
