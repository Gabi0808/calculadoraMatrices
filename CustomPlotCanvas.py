from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class CustomPlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        # Crear una figura y un eje para graficar
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        # Configurar el rango inicial de los ejes
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)

        # Inicializar la cuadrícula y los ejes
        self.ax.grid(True)
        self.ax.axhline(0, color='black', linewidth=0.4)
        self.ax.axvline(0, color='black', linewidth=0.4)

        # Variable para evitar la recursión infinita en pan_limit
        self.is_panning = False

        # Configurar el canvas de matplotlib en PyQt5
        super().__init__(self.fig)
        self.setParent(parent)

        # Conectar los eventos de cambio de límites para limitar el pan
        self.ax.callbacks.connect('xlim_changed', self.on_pan)
        self.ax.callbacks.connect('ylim_changed', self.on_pan)

        # Dibujar el canvas
        self.draw()

    def adjust_ticks_and_limits(self):
        """Ajustar los ticks y límites en función del nivel de zoom y el rango visible."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Limitar el rango a -50 a 50 y establecer ticks de 10 en 10 si se sale del rango
        if xlim[0] < -50 or xlim[1] > 50 or ylim[0] < -50 or ylim[1] > 50:
            # Restringir los límites a -50, 50 en ambos ejes
            self.ax.set_xlim(-50, 50)
            self.ax.set_ylim(-50, 50)
            x_tick_interval = 10
            y_tick_interval = 10
        else:
            # Calcular el rango visible en los ejes
            x_range = xlim[1] - xlim[0]
            y_range = ylim[1] - ylim[0]

            # Determinar el intervalo de los ticks en función del rango visible
            def determine_tick_interval(range_value):
                if range_value <= 2:
                    return 0.2
                elif range_value <= 5:
                    return 0.5
                elif range_value <= 10:
                    return 1
                elif range_value <= 20:
                    return 2
                elif range_value <= 50:
                    return 5
                else:
                    return 10

            x_tick_interval = determine_tick_interval(x_range)
            y_tick_interval = determine_tick_interval(y_range)

        # Generar los ticks tomando el 0 como referencia
        x_ticks = [tick for tick in self._frange_from_zero(xlim[0], xlim[1], x_tick_interval)]
        y_ticks = [tick for tick in self._frange_from_zero(ylim[0], ylim[1], y_tick_interval)]

        # Configurar los ticks en los ejes X e Y
        self.ax.set_xticks(x_ticks)
        self.ax.set_yticks(y_ticks)

        # Redibujar el canvas para actualizar los ticks y límites
        self.draw()

    def _frange_from_zero(self, start, stop, step):
        """Generador para crear una lista de ticks con un paso específico desde 0 como referencia."""
        ticks = []
        current_positive = 0
        current_negative = 0

        while current_positive <= stop:
            if current_positive >= start:
                ticks.append(round(current_positive, 10))
            current_positive += step

        while current_negative >= start:
            if current_negative <= stop:
                ticks.append(round(current_negative, 10))
            current_negative -= step

        return sorted(ticks)

    def wheelEvent(self, event):
        # Obtener el nivel de zoom
        zoom_factor = 1.1 if event.angleDelta().y() < 0 else 0.9  # Aumenta si rueda hacia arriba, disminuye si rueda hacia abajo

        # Obtener el rango actual de los ejes
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Calcular el nuevo rango con el factor de zoom
        new_xrange = [(xlim[0] + xlim[1]) / 2 + (val - (xlim[0] + xlim[1]) / 2) * zoom_factor for val in xlim]
        new_yrange = [(ylim[0] + ylim[1]) / 2 + (val - (ylim[0] + ylim[1]) / 2) * zoom_factor for val in ylim]

        # Aplicar el nuevo rango, limitando a -50, 50 si se intenta hacer zoom out más allá del límite
        if new_xrange[0] < -50 and new_xrange[1] > 50 and new_yrange[0] < -50 and new_yrange[1] > 50:
            self.ax.set_xlim(-50, 50)
            self.ax.set_ylim(-50, 50)
        else:
            self.ax.set_xlim(new_xrange)
            self.ax.set_ylim(new_yrange)

        # Ajustar los ticks y redibujar el canvas
        self.adjust_ticks_and_limits()

    def on_pan(self, ax):
        """Llamado cuando cambia el límite de pan para restringir el movimiento y ajustar los ticks."""
        if not self.is_panning:  # Solo proceder si no estamos en proceso de pan
            self.is_panning = True
            try:
                # Ajustar los límites de pan
                self.pan_limit()
            finally:
                self.is_panning = False  # Restablecer la bandera

            # Ajustar los ticks después de limitar el pan
            self.adjust_ticks_and_limits()


    def pan_limit(self):
        """Limita el pan dentro de los límites de -50 a 50 en ambos ejes sin hacer zoom."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        x_range = xlim[1] - xlim[0]
        y_range = ylim[1] - ylim[0]

        # Calcular los límites permitidos para el pan en función del intervalo y el rango visible
        if xlim[0] < -50:
            self.ax.set_xlim(-50, -50 + x_range)
        elif xlim[1] > 50:
            self.ax.set_xlim(50 - x_range, 50)

        if ylim[0] < -50:
            self.ax.set_ylim(-50, -50 + y_range)
        elif ylim[1] > 50:
            self.ax.set_ylim(50 - y_range, 50)

        # Ajustar los ticks después de limitar el pan
        self.adjust_ticks_and_limits()