import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

class PantallaInventarios(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=30)
        
        # ---- ENCABEZADO ----
        lbl_titulo = tk.Label(self, text="Sistemas de Inventarios", font=("Arial", 18, "bold"), fg="#2c3e50")
        lbl_titulo.pack(anchor="w", pady=(0, 10))
        
        divisor = tk.Frame(self, height=2, bg="#1abc9c")
        divisor.pack(fill="x", pady=(0, 15))
        
        lbl_desc = tk.Label(self, text="📦 Calculadora de Lote Económico (Modelo EOQ / Wilson)", font=("Arial", 11, "italic"), fg="#7f8c8d")
        lbl_desc.pack(anchor="w", pady=(0, 20))

        # ---- CONTENEDOR DE FORMULARIO (INPUTS) ----
        frame_inputs = ttk.LabelFrame(self, text=" Variables del Modelo ", padding=15)
        frame_inputs.pack(fill="x", pady=(0, 20))

        # Demanda Anual (D)
        lbl_demanda = tk.Label(frame_inputs, text="Demanda anual (D) [Unidades/Año]:", font=("Arial", 10))
        lbl_demanda.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.entry_demanda = ttk.Entry(frame_inputs, width=15)
        self.entry_demanda.grid(row=0, column=1, pady=5, padx=5)
        self.entry_demanda.insert(0, "1200")  # Ejemplo: 1200 unidades al año

        # Costo de Ordenar / Pedir (S)
        lbl_costo_pedir = tk.Label(frame_inputs, text="Costo por emitir un pedido (S) [$]:", font=("Arial", 10))
        lbl_costo_pedir.grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.entry_costo_pedir = ttk.Entry(frame_inputs, width=15)
        self.entry_costo_pedir.grid(row=1, column=1, pady=5, padx=5)
        self.entry_costo_pedir.insert(0, "25")  # Ejemplo: $25 por cada llamada/envío

        # Costo de Mantener Inventario (H)
        lbl_costo_mantener = tk.Label(frame_inputs, text="Costo anual de mantener unidad (H) [$]:", font=("Arial", 10))
        lbl_costo_mantener.grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.entry_costo_mantener = ttk.Entry(frame_inputs, width=15)
        self.entry_costo_mantener.grid(row=2, column=1, pady=5, padx=5)
        self.entry_costo_mantener.insert(0, "2.5")  # Ejemplo: $2.5 al año por artículo guardado

        # Botón para Calcular
        btn_calcular = ttk.Button(frame_inputs, text="Calcular Políticas de Inventario", command=self.calcular_eoq)
        btn_calcular.grid(row=3, column=0, columnspan=2, pady=(15, 5))

        # ---- CONTENEDOR DE RESULTADOS ----
        self.frame_resultados = ttk.LabelFrame(self, text=" Resultados de Optimización ", padding=15)
        self.frame_resultados.pack(fill="both", expand=True)

        # Variables reactivas para el texto dinámicamente
        self.res_q = tk.StringVar(value="-")
        self.res_n = tk.StringVar(value="-")
        self.res_t = tk.StringVar(value="-")
        self.res_costo_total = tk.StringVar(value="-")

        # Grid estructurado de resultados
        self.crear_fila_resultado("Cantidad óptima de pedido (Q*):", self.res_q, 0)
        self.crear_fila_resultado("Número esperado de pedidos al año (N):", self.res_n, 1)
        self.crear_fila_resultado("Tiempo entre pedidos (T):", self.res_t, 2)
        self.crear_fila_resultado("Costo total anual de gestión [$]:", self.res_costo_total, 3)

    def crear_fila_resultado(self, texto, variable, fila):
        """Genera filas de manera ordenada en la sección de resultados."""
        lbl_nom = tk.Label(self.frame_resultados, text=texto, font=("Arial", 10, "bold"), fg="#34495e")
        lbl_nom.grid(row=fila, column=0, sticky="w", pady=6, padx=10)
        
        lbl_val = tk.Label(self.frame_resultados, textvariable=variable, font=("Arial", 10), fg="#2980b9")
        lbl_val.grid(row=fila, column=1, sticky="w", pady=6, padx=10)

    def calcular_eoq(self):
        """Aplica la fórmula de Harris-Wilson para resolver el lote óptimo."""
        try:
            # Obtener y parsear los datos ingresados
            d = float(self.entry_demanda.get())
            s = float(self.entry_costo_pedir.get())
            h = float(self.entry_costo_mantener.get())

            # Validar que no existan valores negativos o ceros divisores
            if d <= 0 or s <= 0 or h <= 0:
                raise ValueError("Los valores deben ser estrictamente mayores a cero.")

            # ---- FÓRMULAS MATEMÁTICAS EOQ ----
            # Q* = Raíz cuadrada de (2 * D * S / H)
            q_optimo = math.sqrt((2 * d * s) / h)
            
            # Número de pedidos al año (N = D / Q)
            n_pedidos = d / q_optimo
            
            # Tiempo entre pedidos en días (T = (Q / D) * 365 días)
            tiempo_dias = (q_optimo / d) * 365
            
            # Costo Total = Costo de pedir + Costo de mantener
            # CT = (D/Q)*S + (Q/2)*H
            costo_pedir_total = (d / q_optimo) * s
            costo_mantener_total = (q_optimo / 2) * h
            costo_total = costo_pedir_total + costo_mantener_total

            # ---- ACTUALIZAR TEXTOS EN PANTALLA ----
            self.res_q.set(f"{q_optimo:.2f} unidades por orden")
            self.res_n.set(f"{n_pedidos:.2f} pedidos/año")
            self.res_t.set(f"{tiempo_dias:.1f} días de intervalo")
            self.res_costo_total.set(f"$ {costo_total:.2f} (Pedir: ${costo_pedir_total:.2f} | Mantener: ${costo_mantener_total:.2f})")

        except ValueError:
            messagebox.showerror("Error de Datos", "Por favor, introduce números válidos y mayores a cero en todos los campos.")
