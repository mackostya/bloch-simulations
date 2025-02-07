import tkinter as tk
from tkinter import ttk
import cv2
import matplotlib

matplotlib.use("TkAgg")  # Use the TkAgg backend for embedding plots in Tkinter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from . import utils_fft as utils


# ----------------------------
# Main Tkinter Application
# ----------------------------
class FrequencyFilterApp:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Interactive Frequency Filtering (3-Panel View)")

        # Load / create image and compute its FFT
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.img = cv2.resize(img, (img.shape[1] // 10, img.shape[0] // 10))
        self.F_shifted = utils.fft_image(self.img)

        # Prepare main frames
        self.control_frame = ttk.Frame(root, padding=5)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.plot_frame = ttk.Frame(root, padding=5)
        self.plot_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Set up Matplotlib figure with 3 subplots: [Original, K-space, Reconstructed]
        self.fig, self.axs = plt.subplots(1, 3, figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # UI Elements
        self.filter_label = ttk.Label(self.control_frame, text="Filter Type:")
        self.filter_label.pack(pady=2)

        self.filter_type = tk.StringVar(value="Low-pass")
        self.filter_combo = ttk.OptionMenu(
            self.control_frame,
            self.filter_type,
            "Low-pass",
            "Low-pass",
            "High-pass",
            "Single-freq",
            command=lambda _: self.update_plot(),
        )
        self.filter_combo.pack(pady=2)

        # Cutoff or band radius
        ttk.Label(self.control_frame, text="Cutoff / Band Radius").pack(pady=2)
        self.cutoff_scale = tk.Scale(
            self.control_frame, from_=1, to=128, orient=tk.HORIZONTAL, command=lambda _: self.update_plot()
        )
        self.cutoff_scale.set(20)
        self.cutoff_scale.pack(pady=2, fill=tk.X)

        # Frequency X
        ttk.Label(self.control_frame, text="Freq X").pack(pady=2)
        self.freq_x_scale = tk.Scale(
            self.control_frame, from_=-128, to=128, orient=tk.HORIZONTAL, command=lambda _: self.update_plot()
        )
        self.freq_x_scale.set(30)
        self.freq_x_scale.pack(pady=2, fill=tk.X)

        # Frequency Y
        ttk.Label(self.control_frame, text="Freq Y").pack(pady=2)
        self.freq_y_scale = tk.Scale(
            self.control_frame, from_=-128, to=128, orient=tk.HORIZONTAL, command=lambda _: self.update_plot()
        )
        self.freq_y_scale.set(30)
        self.freq_y_scale.pack(pady=2, fill=tk.X)

        # Initial plot
        self.update_plot()

    def update_plot(self):
        # Clear subplots
        for ax in self.axs:
            ax.clear()

        # Read UI controls
        ftype = self.filter_type.get()
        cutoff = self.cutoff_scale.get()
        fx = self.freq_x_scale.get()
        fy = self.freq_y_scale.get()

        # Apply selected filter
        if ftype == "Low-pass":
            F_filt = utils.low_pass_filter(self.F_shifted, cutoff)
            title = f"Low-pass (cutoff={cutoff})"
        elif ftype == "High-pass":
            F_filt = utils.high_pass_filter(self.F_shifted, cutoff)
            title = f"High-pass (cutoff={cutoff})"
        else:  # Single-freq
            F_filt = utils.select_single_frequency(self.F_shifted, fx, fy, cutoff)
            title = f"Single-freq (fx={fx}, fy={fy}, band={cutoff})"

        # Reconstruct image from filtered k-space
        reconstructed = utils.ifft_image(F_filt)

        # Convert to log magnitude for display (to avoid large dynamic range)
        kspace_log = np.log(1 + np.abs(F_filt))

        # 1) Original Image
        self.axs[0].imshow(self.img, cmap="gray", aspect="auto")
        self.axs[0].set_title("Original Image")
        self.axs[0].axis("off")

        # 2) Filtered K-space
        self.axs[1].imshow(kspace_log, cmap="gray", aspect="auto")
        self.axs[1].set_title("Filtered K-space")
        self.axs[1].axis("off")

        # 3) Reconstructed Image
        self.axs[2].imshow(reconstructed, cmap="gray", aspect="auto")
        self.axs[2].set_title(title)
        self.axs[2].axis("off")

        self.fig.tight_layout()
        self.canvas.draw()
