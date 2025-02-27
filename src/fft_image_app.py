import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont  # For adjusting default Tkinter fonts

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
        # -------------------------------
        # 1) Increase default Tkinter font
        # -------------------------------
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=20)  # Set desired size (e.g., 12, 14, 16, etc.)

        # -------------------------------
        # 2) Increase default Matplotlib font
        # -------------------------------
        matplotlib.rcParams.update({"font.size": 20})  # Adjust global font size for plots

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

        # UI: Filter Type
        self.filter_label = ttk.Label(self.control_frame, text="Filter Type:")
        self.filter_label.pack(pady=2)

        # optionMenuStyle = ttk.Style()
        # optionMenuStyle.configure("my.TMenubutton", font=("Arial", 30, "bold"))

        self.filter_type = tk.StringVar(value="Low-pass")
        self.filter_combo = ttk.OptionMenu(
            self.control_frame,
            self.filter_type,
            "Low-pass",
            "Low-pass",
            "High-pass",
            "Single-freq",
            command=lambda _: self.update_plot(),
            # style="my.TMenubutton",
        )
        self.filter_combo.pack(pady=2)

        # We'll link sliders and Entries via IntVar (or DoubleVar if needed).
        # For each parameter, we create a small sub-frame with a label, scale, and entry.

        # -- Cutoff / Band Radius --
        self.create_param_widget(
            label_text="Cutoff",
            from_=1,
            to=128,
            initial=20,
            callback=self.update_plot,
            var_name="cutoff_var",
        )

        # -- Freq X --
        self.create_param_widget(
            label_text="Freq X",
            from_=-128,
            to=128,
            initial=30,
            callback=self.update_plot,
            var_name="freq_x_var",
        )

        # -- Freq Y --
        self.create_param_widget(
            label_text="Freq Y",
            from_=-128,
            to=128,
            initial=30,
            callback=self.update_plot,
            var_name="freq_y_var",
        )

        # Initial plot
        self.update_plot()

    def create_param_widget(self, label_text, from_, to, initial, callback, var_name):
        """
        Helper to create a sub-frame with:
         - label
         - scale
         - numeric entry
        Binds them all to the same tk.IntVar for easy sync.
        """
        frame = ttk.Frame(self.control_frame)
        frame.pack(pady=2, fill=tk.X)

        label = ttk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT, padx=2)

        # Shared variable
        var = tk.IntVar(value=initial)
        setattr(self, var_name, var)  # store it as an attribute of the class

        # Update function for the scale
        def on_scale_update(value):
            # Attempt to parse as int
            try:
                var.set(int(float(value)))
                callback()
            except ValueError:
                pass

        # The slider/scale
        scale = tk.Scale(
            frame, from_=from_, to=to, orient=tk.HORIZONTAL, variable=var, command=on_scale_update, length=150
        )
        scale.pack(side=tk.LEFT, padx=2)

        # The numeric entry
        entry = ttk.Entry(frame, width=5, textvariable=var)
        entry.pack(side=tk.LEFT, padx=2)

        # When user presses Enter in the entry, refresh
        def on_entry_return(event):
            callback()

        entry.bind("<Return>", on_entry_return)

    def update_plot(self, *args):
        # Clear subplots
        for ax in self.axs:
            ax.clear()

        # Read UI controls
        ftype = self.filter_type.get()
        cutoff = self.cutoff_var.get()
        fx = self.freq_x_var.get()
        fy = self.freq_y_var.get()

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
