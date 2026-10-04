import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class PantallaNoParametricas(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=30)
        
        # ---- ENCABEZADO ----
        lbl_titulo = tk.Label(self, text="Pruebas No Paramétricas", font=("Arial", 18, "bold"), fg="#2c3e50")
        lbl_titulo.pack(anchor="w", pady=(0, 10))
        
        divisor = tk.Frame(self, height=2, bg="#1abc9c")
        divisor.pack(fill="x", pady=(0, 15))
        
        lbl_desc = tk.Label(self, text="📈 Prueba de Chi-cuadrada (χ²) de Bondad de Ajuste", font=("Arial", 11, "italic"), fg="#7f8c8d")
        lbl_desc.pack(anchor="w", pady=(0, 20))

        # ---- CONTENEDOR DE INPUTS ----
        frame_inputs = ttk.LabelFrame(self, text=" Frecuencias de las Categorías ", padding=15)
        frame_inputs.pack(fill="x", pady=(0, 20))

        # Frecuencias Observadas (O)
        lbl_observadas = tk.Label(frame_inputs, text="Frecuencias Observadas (separadas por comas):", font=("Arial", 10))
        lbl_observadas.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.entry_observadas = ttk.Entry(frame_inputs, width=40)
        self.entry_observadas.grid(row=0, column=1, pady=5, padx=5)
        self.entry_observadas.insert(0, "40, 30, 20, 10") # Ejemplo por defecto

        # Frecuencias Esperadas (E)
        lbl_esperadas = tk.Label(frame_inputs, text="Frecuencias Esperadas (separadas por comas):", font=("Arial", 10))
        lbl_esperadas.grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.entry_esperadas = ttk.Entry(frame_inputs, width=40)
        self.entry_esperadas.grid(row=1, column=1, pady=5, padx=5)
        self.entry_esperadas.insert(0, "25, 25, 25, 25") # Ejemplo uniforme por defecto

        # Botón para Calcular
        btn_calcular = ttk.Button(frame_inputs, text="Calcular Chi-cuadrada", command=self.calcular_chi_cuadrada)
        btn_calcular.grid(row=2, column=0, columnspan=2, pady=(15, 5))

        # ---- CONTENEDOR DE RESULTADOS ----
        self.frame_resultados = ttk.LabelFrame(self, text=" Resultados Estadísticos No Paramétricos ", padding=15)
        self.frame_resultados.pack(fill="both", expand=True)

        # Variables reactivas para actualización en pantalla
        self.res_categorias = tk.StringVar(value="-")
        self.res_suma_o = tk.StringVar(value="-")
        self.res_suma_e = tk.StringVar(value="-")
        self.res_gl = tk.StringVar(value="-")
        self.res_chi_calc = tk.StringVar(value="-")

        # Grid de resultados
        self.crear_fila_resultado("Número de categorías (k):", self.res_categorias, 0)
        self.crear_fila_resultado("Suma de frec. observadas (ΣO):", self.res_suma_o, 1)
        self.crear_fila_resultado("Suma de frec. esperadas (ΣE):", self.res_suma_e, 2)
        self.crear_fila_resultado("Grados de libertad (k - 1):", self.res_gl, 3)
        self.crear_fila_resultado("Estadístico χ² calculado:", self.res_chi_calc, 4)

    def crear_fila_resultado(self, texto, variable, fila):
        """Genera filas de manera ordenada en la sección de resultados."""
        lbl_nom = tk.Label(self.frame_resultados, text=texto, font=("Arial", 10, "bold"), fg="#34495e")
        lbl_nom.grid(row=fila, column=0, sticky="w", pady=5, padx=10)
        
        lbl_val = tk.Label(self.frame_resultados, textvariable=variable, font=("Arial", 10), fg="#8e44ad")
        lbl_val.grid(row=fila, column=1, sticky="w", pady=5, padx=10)

    def calcular_chi_cuadrada(self):
        """Lógica para la fórmula de Chi-cuadrada: Σ [ (O - E)² / E ]"""
        try:
            # 1. Parsear los arreglos de texto de entrada
            txt_o = self.entry_observadas.get()
            txt_e = self.entry_esperadas.get()
            
            observadas = [float(x.strip()) for x in txt_o.split(",") if x.strip() != ""]
            esperadas = [float(x.strip()) for x in txt_e.split(",") if x.strip() != ""]

            # 2. Validaciones lógicas iniciales
            if len(observadas) != len(esperadas):
                raise ValueError("La cantidad de categorías observadas debe coincidir con las esperadas.")
            
            k = len(observadas)
            if k < 2:
                raise ValueError("Se requieren al menos 2 categorías para realizar la prueba.")

            if any(e <= 0 for e in esperadas):
                raise ValueError("Las frecuencias esperadas deben ser mayores estrictamente a cero.")

            # Validación de teoría estadística clásica: ΣO debe ser idealmente igual a ΣE
            suma_o = sum(observadas)
            suma_e = sum(esperadas)
            
            if abs(suma_o - suma_e) > 0.001:
                # Si no coinciden, se advierte pero se permite el cálculo o se calcula un aviso comercial
                messagebox.showwarning(
                    "Aviso Estadístico", 
                    f"La suma de Observados ({suma_o}) no es igual a la de Esperados ({suma_e}).\n"
                    "Por rigor metodológico, las muestras totales deberían coincidir."
                )

            # ---- FÓRMULA DE CHI-CUADRADA ----
            chi_calculado = 0.0
            for o, e in zip(observadas, esperadas):
                chi_calculado += ((o - e) ** 2) / e

            gl = k - 1

            # ---- ACTUALIZAR INTERFAZ ----
            self.res_categorias.set(f"{k}")
            self.res_suma_o.set(f"{suma_o:.1f}")
            self.res_suma_e.set(f"{suma_e:.1f}")
            self.res_gl.set(f"{gl}")
            self.res_chi_calc.set(f"{chi_calculado:.4f}")

        except ValueError as e:
            msg = str(e) if "categorías" in str(e) or "coincidir" in str(e) or "mayores" in str(e) else "Por favor ingresa listas válidas de números separados por comas."
            messagebox.showerror("Error en el Análisis", msg)
