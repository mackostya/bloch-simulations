import tkinter as tk
from src.fft_image_app import FrequencyFilterApp


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
