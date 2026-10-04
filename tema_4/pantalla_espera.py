import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class PantallaEspera(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=30)
        
        # ---- ENCABEZADO ----
        lbl_titulo = tk.Label(self, text="Problemas con Líneas de Espera", font=("Arial", 18, "bold"), fg="#2c3e50")
        lbl_titulo.pack(anchor="w", pady=(0, 10))
        
        divisor = tk.Frame(self, height=2, bg="#1abc9c")
        divisor.pack(fill="x", pady=(0, 15))
        
        lbl_desc = tk.Label(self, text="⏳ Calculadora del Modelo M/M/1 (Un solo servidor)", font=("Arial", 11, "italic"), fg="#7f8c8d")
        lbl_desc.pack(anchor="w", pady=(0, 20))

        # ---- CONTENEDOR DE FORMULARIO (INPUTS) ----
        frame_inputs = ttk.LabelFrame(self, text=" Datos de Entrada ", padding=15)
        frame_inputs.pack(fill="x", pady=(0, 20))

        # Tasa de Llegada (Lambda)
        lbl_lambda = tk.Label(frame_inputs, text="Tasa de llegada (λ) [Clientes/Hora]:", font=("Arial", 10))
        lbl_lambda.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.entry_lambda = ttk.Entry(frame_inputs, width=15)
        self.entry_lambda.grid(row=0, column=1, pady=5, padx=5)
        self.entry_lambda.insert(0, "12") # Ejemplo por defecto

        # Tasa de Servicio (Mu)
        lbl_mu = tk.Label(frame_inputs, text="Tasa de servicio (μ) [Clientes/Hora]:", font=("Arial", 10))
        lbl_mu.grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.entry_mu = ttk.Entry(frame_inputs, width=15)
        self.entry_mu.grid(row=1, column=1, pady=5, padx=5)
        self.entry_mu.insert(0, "15") # Ejemplo por defecto (Debe ser mayor a Lambda)

        # Botón para Calcular
        btn_calcular = ttk.Button(frame_inputs, text="Calcular Métricas", command=self.calcular_mm1)
        btn_calcular.grid(row=2, column=0, columnspan=2, pady=(15, 5))

        # ---- CONTENEDOR DE RESULTADOS ----
        self.frame_resultados = ttk.LabelFrame(self, text=" Métricas del Sistema ", padding=15)
        self.frame_resultados.pack(fill="both", expand=True)

        # Variables para actualizar el texto dinámicamente
        self.res_l = tk.StringVar(value="-")
        self.res_lq = tk.StringVar(value="-")
        self.res_w = tk.StringVar(value="-")
        self.res_wq = tk.StringVar(value="-")
        self.res_rho = tk.StringVar(value="-")

        # Grid de resultados
        self.crear_fila_resultado("Utilización del sistema (ρ):", self.res_rho, 0)
        self.crear_fila_resultado("Promedio de clientes en el sistema (L):", self.res_l, 1)
        self.crear_fila_resultado("Promedio de clientes en la cola (Lq):", self.res_lq, 2)
        self.crear_fila_resultado("Tiempo promedio en el sistema (W):", self.res_w, 3)
        self.crear_fila_resultado("Tiempo promedio en la cola (Wq):", self.res_wq, 4)

    def crear_fila_resultado(self, texto, variable, fila):
        """Genera filas de manera ordenada en la sección de resultados."""
        lbl_nom = tk.Label(self.frame_resultados, text=texto, font=("Arial", 10, "bold"), fg="#34495e")
        lbl_nom.grid(row=fila, column=0, sticky="w", pady=6, padx=10)
        
        lbl_val = tk.Label(self.frame_resultados, textvariable=variable, font=("Arial", 10), fg="#16a085")
        lbl_val.grid(row=fila, column=1, sticky="w", pady=6, padx=10)

    def calcular_mm1(self):
        """Lógica matemática para resolver el modelo de líneas de espera M/M/1."""
        try:
            # Obtener valores de la interfaz
            lam = float(self.entry_lambda.get())
            mu = float(self.entry_mu.get())

            # Validaciones lógicas básicas de teoría de colas
            if lam <= 0 or mu <= 0:
                raise ValueError("Los valores deben ser mayores a cero.")
            
            if lam >= mu:
                messagebox.showerror(
                    "Error de Sistema", 
                    "La tasa de llegada (λ) debe ser MENOR que la tasa de servicio (μ).\n"
                    "De lo contrario, la cola crecería indefinidamente y el sistema colapsaría."
                )
                return

            # ---- FÓRMULAS M/M/1 ----
            rho = lam / mu                      # Factor de utilización
            l_val = lam / (mu - lam)            # Clientes promedio en el sistema
            lq_val = (lam**2) / (mu * (mu - lam)) # Clientes promedio en la cola
            w_val = 1 / (mu - lam)              # Tiempo promedio en el sistema (horas)
            wq_val = lam / (mu * (mu - lam))    # Tiempo promedio en la cola (horas)

            # Convertir tiempos a minutos para que sea más legible
            w_min = w_val * 60
            wq_min = wq_val * 60

            # ---- ACTUALIZAR INTERFAZ ----
            self.res_rho.set(f"{rho * 100:.2f} % (Ocupado)")
            self.res_l.set(f"{l_val:.2f} clientes")
            self.res_lq.set(f"{lq_val:.2f} clientes")
            self.res_w.set(f"{w_val:.3f} hrs ({w_min:.1f} minutos)")
            self.res_wq.set(f"{wq_val:.3f} hrs ({wq_min:.1f} minutos)")

        except ValueError:
            messagebox.showerror("Error de Datos", "Por favor, introduce únicamente números válidos en los campos.")
