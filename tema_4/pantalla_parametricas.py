import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

class PantallaParametricas(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=30)
        
        # ---- ENCABEZADO ----
        lbl_titulo = tk.Label(self, text="Pruebas Paramétricas", font=("Arial", 18, "bold"), fg="#2c3e50")
        lbl_titulo.pack(anchor="w", pady=(0, 10))
        
        divisor = tk.Frame(self, height=2, bg="#1abc9c")
        divisor.pack(fill="x", pady=(0, 15))
        
        lbl_desc = tk.Label(self, text="📊 Prueba t de Student (Para una Muestra)", font=("Arial", 11, "italic"), fg="#7f8c8d")
        lbl_desc.pack(anchor="w", pady=(0, 20))

        # ---- CONTENEDOR DE INPUTS ----
        frame_inputs = ttk.LabelFrame(self, text=" Datos de la Muestra ", padding=15)
        frame_inputs.pack(fill="x", pady=(0, 20))

        # Ingreso de datos (Lista separada por comas)
        lbl_datos = tk.Label(frame_inputs, text="Datos de la muestra (separados por comas):", font=("Arial", 10))
        lbl_datos.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.entry_datos = ttk.Entry(frame_inputs, width=40)
        self.entry_datos.grid(row=0, column=1, pady=5, padx=5)
        self.entry_datos.insert(0, "10.5, 11.2, 9.8, 10.1, 10.7, 11.0, 9.9") # Ejemplo por defecto

        # Media Hipotética (Mu_0)
        lbl_mu0 = tk.Label(frame_inputs, text="Media poblacional hipotética (μ₀):", font=("Arial", 10))
        lbl_mu0.grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.entry_mu0 = ttk.Entry(frame_inputs, width=15)
        self.entry_mu0.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        self.entry_mu0.insert(0, "10.0") # Ejemplo por defecto

        # Botón para Calcular
        btn_calcular = ttk.Button(frame_inputs, text="Calcular Prueba t", command=self.calcular_prueba_t)
        btn_calcular.grid(row=2, column=0, columnspan=2, pady=(15, 5))

        # ---- CONTENEDOR DE RESULTADOS ----
        self.frame_resultados = ttk.LabelFrame(self, text=" Resultados Estadísticos ", padding=15)
        self.frame_resultados.pack(fill="both", expand=True)

        # Variables reactivas para el texto
        self.res_n = tk.StringVar(value="-")
        self.res_media = tk.StringVar(value="-")
        self.res_desviacion = tk.StringVar(value="-")
        self.res_gl = tk.StringVar(value="-")
        self.res_t_calc = tk.StringVar(value="-")

        # Grid de resultados
        self.crear_fila_resultado("Tamaño de muestra (n):", self.res_n, 0)
        self.crear_fila_resultado("Media muestral (x̄):", self.res_media, 1)
        self.crear_fila_resultado("Desviación estándar (s):", self.res_desviacion, 2)
        self.crear_fila_resultado("Grados de libertad (gl):", self.res_gl, 3)
        self.crear_fila_resultado("Estadístico t calculado (t_calc):", self.res_t_calc, 4)

    def crear_fila_resultado(self, texto, variable, fila):
        """Genera filas de manera ordenada en la sección de resultados."""
        lbl_nom = tk.Label(self.frame_resultados, text=texto, font=("Arial", 10, "bold"), fg="#34495e")
        lbl_nom.grid(row=fila, column=0, sticky="w", pady=5, padx=10)
        
        lbl_val = tk.Label(self.frame_resultados, textvariable=variable, font=("Arial", 10), fg="#d35400")
        lbl_val.grid(row=fila, column=1, sticky="w", pady=5, padx=10)

    def calcular_prueba_t(self):
        """Calcula de forma nativa la media, desviación estándar y el valor t."""
        try:
            # 1. Parsear y limpiar la lista de datos ingresada
            texto_datos = self.entry_datos.get()
            datos = [float(x.strip()) for x in texto_datos.split(",") if x.strip() != ""]
            
            # 2. Obtener media hipotética
            mu0 = float(self.entry_mu0.get())

            n = len(datos)
            if n < 2:
                raise ValueError("Se necesitan al menos 2 datos para realizar la prueba.")

            # ---- CÁLCULOS ESTADÍSTICOS DESDE CERO ----
            # Media muestral
            media = sum(datos) / n
            
            # Desviación estándar muestral (s) con corrección de Bessel (n-1)
            varianza_suma = sum((x - media) ** 2 for x in datos)
            desviacion = math.sqrt(varianza_suma / (n - 1))
            
            if desviacion == 0:
                raise ValueError("La desviación estándar es 0 (todos los datos son iguales). No se puede calcular t.")

            # Grados de libertad
            gl = n - 1

            # Estadístico t calculado: t = (x̄ - μ₀) / (s / √n)
            error_estandar = desviacion / math.sqrt(n)
            t_calculado = (media - mu0) / error_estandar

            # ---- ACTUALIZAR INTERFAZ ----
            self.res_n.set(f"{n}")
            self.res_media.set(f"{media:.4f}")
            self.res_desviacion.set(f"{desviacion:.4f}")
            self.res_gl.set(f"{gl}")
            self.res_t_calc.set(f"{t_calculado:.4f}")

        except ValueError as e:
            # Capturar errores de conversión o lógicos
            msg = str(e) if "datos" in str(e) or "desviación" in str(e) or "al menos" in str(e) else "Asegúrate de ingresar solo números separados por comas."
            messagebox.showerror("Error en los Datos", msg)
