from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QSlider, QGridLayout, QVBoxLayout, QGroupBox

from src.qt.widgets import KSpaceWidget, SpinWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spin Dephasing Demo")

        self.kspace_widget = KSpaceWidget()
        self.spin_widget = SpinWidget()

        # Create QGroupBoxes with titles
        self.kspace_box = QGroupBox("K-Space")
        self.spins_box = QGroupBox("Spins")

        # Layouts for the group boxes
        kspace_layout = QVBoxLayout()
        kspace_layout.addWidget(self.kspace_widget)
        self.kspace_box.setLayout(kspace_layout)

        spins_layout = QVBoxLayout()
        spins_layout.addWidget(self.spin_widget)
        self.spins_box.setLayout(spins_layout)

        # Sliders for Gx, Gy
        self.slider_x = QSlider(Qt.Horizontal)
        self.slider_x.setRange(-20, 20)
        self.slider_x.setValue(0)
        self.slider_x.valueChanged.connect(self.onGradUpdate)

        self.slider_y = QSlider(Qt.Vertical)
        self.slider_y.setRange(-20, 20)
        self.slider_y.setValue(0)
        self.slider_y.valueChanged.connect(self.onGradUpdate)

        # Main layout
        grid = QGridLayout()
        # Row 0: left slider (Gy), and group boxes (k-space, spins)
        grid.addWidget(self.slider_y, 0, 0, 2, 1)
        grid.addWidget(self.kspace_box, 0, 1)
        grid.addWidget(self.spins_box, 0, 2)
        # Row 1: horizontal slider for Gx
        grid.addWidget(self.slider_x, 1, 0, 1, 2)

        container = QWidget()
        container.setLayout(grid)
        self.setCentralWidget(container)

        # Ensure an initial update
        self.onGradUpdate()

    def onGradUpdate(self):
        Gx = self.slider_x.value()
        Gy = self.slider_y.value()

        # Update K-space widget
        self.kspace_widget.setKSpace(Gx, Gy)

        # Update spin widget
        self.spin_widget.setGradients(Gx, Gy)
