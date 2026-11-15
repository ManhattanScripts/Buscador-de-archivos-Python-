import os
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox

def abrir_universal(ruta, abrir_directo=True):
    """Abre un archivo o carpeta de forma compatible con Windows, Linux y macOS."""
    sistema = platform.system()
    
    # Si la opción de abrir directo está desactivada, tomamos la carpeta contenedora
    ruta_a_abrir = ruta if abrir_directo else os.path.dirname(ruta)
    
    if not os.path.exists(ruta_a_abrir):
        messagebox.showerror("Error", f"La ruta no existe: {ruta_a_abrir}")
        return

    try:
        if sistema == "Windows":
            os.startfile(ruta_a_abrir)
        elif sistema == "Darwin":  # macOS
            subprocess.run(["open", ruta_a_abrir])
        else:  # Linux y otros sistemas Unix
            subprocess.run(["xdg-open", ruta_a_abrir])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el elemento: {e}")

def ejecutar_busqueda(entrada_nombre, categoria_var, formato_var, abrir_directo_var, caja_resultado):
    nombre_buscado = entrada_nombre.get().strip()
    categoria_seleccionada = categoria_var.get()
    extension_buscada = formato_var.get().strip().lower()
    abrir_directo = abrir_directo_var.get()
    
    if not nombre_buscado:
        messagebox.showwarning("Atención", "Por favor, escribe el nombre que buscas.")
        return

    # Punto de partida adaptable según el sistema operativo
    if platform.system() == "Windows":
        punto_de_partida = "C:\\"
    else:
        punto_de_partida = "/"  
    
    caja_resultado.config(state="normal")
    caja_resultado.delete(0, tk.END)
    caja_resultado.insert(0, "Buscando elementos...")
    caja_resultado.config(state="readonly")
    caja_resultado.update()

    try:
        for ruta_actual, carpetas, archivos in os.walk(punto_de_partida):
            
           
            if platform.system() == "Windows":
                if "Windows" in carpetas: carpetas.remove("Windows")
                if "$Recycle.Bin" in carpetas: carpetas.remove("$Recycle.Bin")
                if "AppData" in carpetas: carpetas.remove("AppData")
            else:
                
                if "proc" in carpetas: carpetas.remove("proc")
                if "sys" in carpetas: carpetas.remove("sys")
                if "dev" in carpetas: carpetas.remove("dev")

            # MODO 1: Buscar Carpetas
            if categoria_seleccionada == "Carpetas":
                for carpeta in carpetas:
                    if nombre_buscado.lower() in carpeta.lower():
                        ruta_completa = os.path.join(ruta_actual, carpeta)
                        
                        caja_resultado.config(state="normal")
                        caja_resultado.delete(0, tk.END)
                        caja_resultado.insert(0, ruta_completa)
                        caja_resultado.config(state="readonly")
                        
                        abrir_universal(ruta_completa, abrir_directo)
                        return ruta_completa

            # MODO 2: Buscar Archivos
            else:
                for archivo in archivos:
                    nombre_archivo, ext_archivo = os.path.splitext(archivo)
                    
                    if nombre_buscado.lower() in nombre_archivo.lower() and ext_archivo.lower() == extension_buscada:
                        ruta_completa = os.path.join(ruta_actual, archivo)
                        
                        caja_resultado.config(state="normal")
                        caja_resultado.delete(0, tk.END)
                        caja_resultado.insert(0, ruta_completa)
                        caja_resultado.config(state="readonly")
                        
                        abrir_universal(ruta_completa, abrir_directo)
                        return ruta_completa

        caja_resultado.config(state="normal")
        caja_resultado.delete(0, tk.END)
        caja_resultado.insert(0, "No se encontró el elemento.")
        caja_resultado.config(state="readonly")
        
        messagebox.showinfo("Resultado", "El elemento no existe o no se pudo encontrar.")
        return None

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error de acceso: {e}")

# --- VENTANA PRINCIPAL ---
ventana = tk.Tk()
ventana.title("Buscador Inteligente Multiplataforma")
ventana.geometry("520x500")
ventana.config(bg="#f0f0f0")

categorias = {
    "Imágenes (Fotos)": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Audios": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Documentos": [".txt", ".pdf", ".docx", ".xlsx", ".pptx", ".md", ".rtf"],
    "Otros / Código": [".zip", ".rar", ".7z", ".exe", ".py", ".json", ".html", ".js"],
    "Carpetas": ["(Directorio)"]
}

tk.Label(ventana, text="Nombre del archivo o carpeta:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=(15, 5))
caja_nombre = tk.Entry(ventana, width=40, font=("Arial", 11))
caja_nombre.pack()

tk.Label(ventana, text="Selecciona la categoría:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=(15, 5))
categoria_var = tk.StringVar(ventana)
categoria_var.set("Imágenes (Fotos)")
menu_categoria = tk.OptionMenu(ventana, categoria_var, *categorias.keys())
menu_categoria.config(width=28, font=("Arial", 10))
menu_categoria.pack()

tk.Label(ventana, text="Selecciona el formato específico:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=(15, 5))
formato_var = tk.StringVar(ventana)
formato_var.set(categorias["Imágenes (Fotos)"][0])
menu_formato = tk.OptionMenu(ventana, formato_var, "")
menu_formato.config(width=28, font=("Arial", 10))
menu_formato.pack()

def actualizar_formatos(*args):
    cat_elegida = categoria_var.get()
    lista_formatos = categorias.get(cat_elegida, [".txt"])
    
    menu_formato["menu"].delete(0, "end")
    for fmt in lista_formatos:
        menu_formato["menu"].add_command(label=fmt, command=lambda v=fmt: formato_var.set(v))
    
    formato_var.set(lista_formatos[0])
    
    if cat_elegida == "Carpetas":
        menu_formato.config(state="disabled")
    else:
        menu_formato.config(state="normal")

categoria_var.trace_add("write", actualizar_formatos)
actualizar_formatos()

abrir_directo_var = tk.BooleanVar(value=False)  
check_abrir = tk.Checkbutton(
    ventana, 
    text="Abrir archivo / Entrar a la carpeta directamente (en vez de ver ubicación)", 
    variable=abrir_directo_var,
    bg="#f0f0f0",
    font=("Arial", 9)
)
check_abrir.pack(pady=10)

boton_buscar = tk.Button(
    ventana, 
    text="Iniciar Búsqueda", 
    bg="#4CAF50", 
    fg="white", 
    font=("Arial", 11, "bold"),
    padx=10, 
    pady=5,
    command=lambda: ejecutar_busqueda(caja_nombre, categoria_var, formato_var, abrir_directo_var, caja_resultado)
)
boton_buscar.pack(pady=10)

tk.Label(ventana, text="Ruta encontrada (Copiable):", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(pady=(5, 2))
caja_resultado = tk.Entry(ventana, width=58, font=("Arial", 10))
caja_resultado.pack(pady=5)
caja_resultado.config(state="readonly")

ventana.mainloop()