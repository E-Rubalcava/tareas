import tkinter as tk
from tkinter import ttk
import math

class MotorDCSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Motor de Corriente Directa (GUI)")
        self.root.geometry("450x520")
        self.root.resizable(False, False)

        # Variables de estado
        self.encendido = False
        self.sentido = tk.StringVar(value="Horario")  # Horario o Antihorario
        self.velocidad = tk.IntVar(value=50)         # 0 a 100%
        self.angulo = 0.0

        self._crear_widgets()
        self._animar()

    def _crear_widgets(self):
        # Título principal
        lbl_titulo = tk.Label(self.root, text="Panel de Control - Motor DC", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=10)

        # Canvas para representación visual del motor
        self.canvas = tk.Canvas(self.root, width=200, height=200, bg="#202020", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Panel de Estado
        self.frame_estado = ttk.LabelFrame(self.root, text=" Estado del Motor ", padding=10)
        self.frame_estado.pack(fill="x", padx=30, pady=5)

        self.lbl_estado = ttk.Label(self.frame_estado, text="Estado: APAGADO", font=("Arial", 10, "bold"), foreground="red")
        self.lbl_estado.grid(row=0, column=0, sticky="w", padx=10)

        self.lbl_rpm = ttk.Label(self.frame_estado, text="Velocidad: 0%", font=("Arial", 10))
        self.lbl_rpm.grid(row=0, column=1, sticky="e", padx=10)

        # Panel de Controles
        frame_controles = ttk.LabelFrame(self.root, text=" Controles ", padding=10)
        frame_controles.pack(fill="x", padx=30, pady=10)

        # Botones de encendido / apagado
        self.btn_encender = ttk.Button(frame_controles, text="Encender", command=self.encender)
        self.btn_encender.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_apagar = ttk.Button(frame_controles, text="Apagar", command=self.apagar, state="disabled")
        self.btn_apagar.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Sentido de giro
        lbl_dir = ttk.Label(frame_controles, text="Sentido de giro:")
        lbl_dir.grid(row=1, column=0, columnspan=2, pady=(10, 2), sticky="w")

        frame_radio = ttk.Frame(frame_controles)
        frame_radio.grid(row=2, column=0, columnspan=2, sticky="w")
        ttk.Radiobutton(frame_radio, text="Horario (CW)", variable=self.sentido, value="Horario").pack(side="left", padx=5)
        ttk.Radiobutton(frame_radio, text="Antihorario (CCW)", variable=self.sentido, value="Antihorario").pack(side="left", padx=15)

        # Control de Velocidad (Slider)
        lbl_slider = ttk.Label(frame_controles, text="Control PWM / Velocidad (0 - 100%):")
        lbl_slider.grid(row=3, column=0, columnspan=2, pady=(10, 2), sticky="w")

        self.scale_vel = ttk.Scale(frame_controles, from_=0, to=100, orient="horizontal", variable=self.velocidad, command=self._actualizar_velocidad)
        self.scale_vel.grid(row=4, column=0, columnspan=2, sticky="ew")

        frame_controles.columnconfigure(0, weight=1)
        frame_controles.columnconfigure(1, weight=1)

    def encender(self):
        self.encendido = True
        self.btn_encender.config(state="disabled")
        self.btn_apagar.config(state="normal")
        self.lbl_estado.config(text="Estado: ENCENDIDO", foreground="green")
        self._actualizar_velocidad()

    def apagar(self):
        self.encendido = False
        self.btn_encender.config(state="normal")
        self.btn_apagar.config(state="disabled")
        self.lbl_estado.config(text="Estado: APAGADO", foreground="red")
        self.lbl_rpm.config(text="Velocidad: 0%")

    def _actualizar_velocidad(self, *args):
        if self.encendido:
            self.lbl_rpm.config(text=f"Velocidad: {int(self.velocidad.get())}%")

    def _animar(self):
        self.canvas.delete("all")

        cx, cy, r = 100, 100, 75

        # Carcasa exterior del motor
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#555555", width=6, fill="#2b2b2b")

        # Si está encendido, rotar el ángulo en función de la velocidad y dirección
        if self.encendido:
            paso = (self.velocidad.get() / 10.0)
            if self.sentido.get() == "Horario":
                self.angulo = (self.angulo + paso) % 360
            else:
                self.angulo = (self.angulo - paso) % 360

        # Dibujo de aspas / rotor
        rad = math.radians(self.angulo)
        for offset in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
            x_end = cx + (r - 12) * math.cos(rad + offset)
            y_end = cy + (r - 12) * math.sin(rad + offset)
            color = "#00bcd4" if self.encendido else "#777777"
            self.canvas.create_line(cx, cy, x_end, y_end, fill=color, width=4)

        # Núcleo central
        self.canvas.create_oval(cx - 15, cy - 15, cx + 15, cy + 15, fill="#e91e63" if self.encendido else "#555555", outline="white")

        # Tasa de refresco (~50 FPS)
        self.root.after(20, self._animar)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = MotorDCSimulator(ventana)
    ventana.mainloop()