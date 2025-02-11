import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QBrush


class KSpaceWidget(QWidget):
    """Displays a point in k-space, whose coordinates depend on
    (Gx, Gy) – the x/y-gradients from the sliders.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.kx = 0
        self.ky = 0

    def setKSpace(self, kx, ky):
        """Update the k-space location and repaint."""
        self.kx = kx
        self.ky = ky
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Draw background
        painter.fillRect(self.rect(), Qt.white)

        # Draw a border
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawRect(self.rect())

        # Map kx, ky (which might be from e.g. -20..20) into widget coords
        w = self.width()
        h = self.height()

        # Suppose we want k-space from -20..20 in both directions
        k_min, k_max = -20, 20
        # Convert (kx, ky) -> pixel coords
        # x goes from left->right, y from top->bottom
        # But typically in math we expect ky up->down negative, so invert Y.
        px = (self.kx - k_min) / (k_max - k_min) * w
        py = (k_max - self.ky) / (k_max - k_min) * h

        # Draw the point in k-space
        point_radius = 6
        painter.setBrush(QBrush(Qt.red))
        # Cast to int:
        painter.drawEllipse(
            int(px - point_radius / 2), int(py - point_radius / 2), int(point_radius), int(point_radius)
        )


class SpinWidget(QWidget):
    """
    Displays a grid of spins (arrows) that rotate/dephase based on
    the current gradients Gx, Gy. For simplicity, we set each spin's
    phase = (Gx * x + Gy * y).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.Gx = 0
        self.Gy = 0

        # Predefine spin positions in a grid
        # e.g. from -5..5 in both x,y.
        self.spin_positions = []
        for i in range(-10, 11):  # -5 to 5 inclusive
            for j in range(-10, 11):
                self.spin_positions.append((i, j))

    def setGradients(self, Gx, Gy):
        """Update the gradient values and repaint spins."""
        self.Gx = Gx
        self.Gy = Gy
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Draw background
        painter.fillRect(self.rect(), Qt.white)

        # Draw a border
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawRect(self.rect())

        # Draw spins
        # We'll map real-space positions in [-10..10] x [-10..10]
        # to widget coordinates:
        w = self.width()
        h = self.height()
        margin = 20

        # For each spin, compute its phase due to Gx*x + Gy*y
        for x, y in self.spin_positions:
            phase = (self.Gx * x + self.Gy * y) * 0.2  # scale factor?

            # Convert (x,y) to pixel coords
            # assume -10..10 => margin..(w - margin)
            px = margin + (x + 10) / 20.0 * (w - 2 * margin)
            py = (h - margin) - (y + 10) / 20.0 * (h - 2 * margin)

            # Draw arrow for the spin
            self.drawArrow(painter, px, py, phase)

    def drawArrow(self, painter, cx, cy, angle):
        """
        Draw a small arrow centered at (cx, cy) pointing
        in the direction given by 'angle' (radians).
        """
        length = 15
        head_size = 6

        # Compute the end of the arrow
        ex = cx + length * math.cos(angle)
        ey = cy - length * math.sin(angle)  # minus because y grows downward

        pen = QPen(Qt.blue, 2)
        painter.setPen(pen)

        # Draw the main shaft
        painter.drawLine(int(cx), int(cy), int(ex), int(ey))

        # Arrowhead lines
        left_head_angle = angle + math.radians(150)
        right_head_angle = angle - math.radians(150)

        lx = ex + head_size * math.cos(left_head_angle)
        ly = ey - head_size * math.sin(left_head_angle)
        rx = ex + head_size * math.cos(right_head_angle)
        ry = ey - head_size * math.sin(right_head_angle)

        painter.drawLine(QPointF(ex, ey), QPointF(lx, ly))
        painter.drawLine(QPointF(ex, ey), QPointF(rx, ry))
