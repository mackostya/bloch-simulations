
import numpy as np
import matplotlib
import tkinter as tk
from src.fft_image_app import FrequencyFilterApp
import cv2


def main():
    try:
        root = tk.Tk()
        app = FrequencyFilterApp(root, "imgs/image.png")
        root.mainloop()
    except KeyboardInterrupt:
        print("Exiting...")
        root.quit()

if __name__ == "__main__":
    main()
