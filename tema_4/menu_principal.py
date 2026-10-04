import tkinter as tk
from tkinter import ttk

# Importamos las pantallas desde los otros archivos
from pantalla_espera import PantallaEspera
from pantalla_inventarios import PantallaInventarios
from pantalla_parametricas import PantallaParametricas
from pantalla_no_parametricas import PantallaNoParametricas

class AppPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Integrado")
        self.root.geometry("850x550")
        self.root.minsize(750, 480)

        # ---- ESTILOS ----
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Menu.TFrame", background="#2c3e50")
        self.style.configure("Menu.TButton", font=("Arial", 11, "bold"), background="#34495e", foreground="white", padding=10)
        self.style.map("Menu.TButton", background=[("active", "#1abc9c"), ("pressed", "#16a085")])

        # ---- ESTRUCTURA DE CONTENEDORES ----
        # Menú lateral
        self.menu_lateral = ttk.Frame(self.root, width=220, style="Menu.TFrame")
        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False)

        # Contenedor para el Notebook
        self.contenedor_derecho = ttk.Frame(self.root)
        self.contenedor_derecho.pack(side="right", expand=True, fill="both")

        # Notebook que alojará los archivos de las pantallas
        self.notebook = ttk.Notebook(self.contenedor_derecho)
        self.notebook.pack(expand=True, fill="both")

        # ---- INSTANCIAR E INTEGRAR PANTALLAS MODULARES ----
        self.pantalla_espera = PantallaEspera(self.notebook)
        self.pantalla_inventarios = PantallaInventarios(self.notebook)
        self.pantalla_parametricas = PantallaParametricas(self.notebook)
        self.pantalla_no_parametricas = PantallaNoParametricas(self.notebook)

        # Añadirlas al contenedor interno indexado
        self.notebook.add(self.pantalla_espera)
        self.notebook.add(self.pantalla_inventarios)
        self.notebook.add(self.pantalla_parametricas)
        self.notebook.add(self.pantalla_no_parametricas)

        # Ocultar pestañas superiores por diseño estético
        self.style.layout("TNotebook.Tab", [])

        # ---- ELEMENTOS DEL MENÚ LATERAL ----
        lbl_menu = tk.Label(self.menu_lateral, text="MENÚ PRINCIPAL", font=("Arial", 12, "bold"), bg="#2c3e50", fg="#ecf0f1", pady=20)
        lbl_menu.pack()

        btn1 = ttk.Button(self.menu_lateral, text="⏳ Líneas de Espera", style="Menu.TButton", command=lambda: self.cambiar_pantalla(0))
        btn1.pack(fill="x", padx=10, pady=5)

        btn2 = ttk.Button(self.menu_lateral, text="📦 Sist. Inventarios", style="Menu.TButton", command=lambda: self.cambiar_pantalla(1))
        btn2.pack(fill="x", padx=10, pady=5)

        btn3 = ttk.Button(self.menu_lateral, text="📊 P. Paramétricas", style="Menu.TButton", command=lambda: self.cambiar_pantalla(2))
        btn3.pack(fill="x", padx=10, pady=5)

        btn4 = ttk.Button(self.menu_lateral, text="📈 P. No Paramétricas", style="Menu.TButton", command=lambda: self.cambiar_pantalla(3))
        btn4.pack(fill="x", padx=10, pady=5)

    def cambiar_pantalla(self, indice):
        self.notebook.select(indice)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppPrincipal(root)
    root.mainloop()
