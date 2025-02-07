import numpy as np
import matplotlib.pyplot as plt
import cv2
from src import utils_fft as utils


def create_synthetic_gradient(width=256, height=256):
    """
    Create a synthetic diagonal gradient image for demonstration.
    """
    # X, Y are indices for the 2D grid
    y = np.linspace(0, 1, height).reshape(-1, 1)
    x = np.linspace(0, 1, width).reshape(1, -1)
    # Combine x and y to form diagonal gradient
    # Feel free to tweak this formula for different patterns
    gradient = x + y
    return gradient


def main():
    # ------------------------------------
    # 1) Load or create a test image
    # ------------------------------------

    # Option A: Use a synthetic gradient image
    # img = create_synthetic_gradient(width=256, height=256)
    # Option B: Load an actual image from diskimage = plt.imread('../imgs/image.png')  # Replace with your image path
    img = cv2.imread("imgs/image.png", 0)
    img = cv2.resize(img, (img.shape[1] // 10, img.shape[0] // 10))

    # ------------------------------------
    # 2) Compute the 2D FFT
    # ------------------------------------
    F_shifted = utils.fft_image(img)

    # ------------------------------------
    # 3) Low-pass filter
    # ------------------------------------
    cutoff_radius_lp = 20
    F_low_pass = utils.low_pass_filter(F_shifted, cutoff_radius_lp)
    img_lp = utils.ifft_image(F_low_pass)

    # ------------------------------------
    # 4) High-pass filter
    # ------------------------------------
    cutoff_radius_hp = 20
    F_high_pass = utils.high_pass_filter(F_shifted, cutoff_radius_hp)
    img_hp = utils.ifft_image(F_high_pass)

    # ------------------------------------
    # 5) Single frequency selection
    #    Example: pick some small offset from center in x & y
    # ------------------------------------
    freq_x, freq_y = 10, 10  # Adjust as needed
    F_single_freq = utils.select_single_frequency(F_shifted, freq_x, freq_y, band_radius=0)
    img_single_freq = utils.ifft_image(F_single_freq)
    img_single_freq = np.real(img_single_freq)

    # ------------------------------------
    # 6) Visualization
    # ------------------------------------
    # Make sure to display the magnitude of the spectrum too, for demonstration
    spectrum = np.log(1 + np.abs(F_shifted))
    spectrum_lp = np.log(1 + np.abs(F_low_pass))
    spectrum_hp = np.log(1 + np.abs(F_high_pass))
    spectrum_single = np.log(1 + np.abs(F_single_freq))

    plt.figure(figsize=(12, 8))

    # Original image
    plt.subplot(2, 4, 1)
    plt.imshow(img, cmap="gray")
    plt.title("Original Image")
    plt.axis("off")

    # FFT Spectrum (shifted)
    plt.subplot(2, 4, 2)
    plt.imshow(spectrum, cmap="gray")
    plt.title("FFT Spectrum")
    plt.axis("off")

    # Low-pass result
    plt.subplot(2, 4, 3)
    plt.imshow(img_lp, cmap="gray")
    plt.title("Low-Pass Reconstruction")
    plt.axis("off")

    # Low-pass spectrum
    plt.subplot(2, 4, 4)
    plt.imshow(spectrum_lp, cmap="gray")
    plt.title("Low-Pass Spectrum")
    plt.axis("off")

    # High-pass result
    plt.subplot(2, 4, 5)
    plt.imshow(img_hp, cmap="gray")
    plt.title("High-Pass Reconstruction")
    plt.axis("off")

    # High-pass spectrum
    plt.subplot(2, 4, 6)
    plt.imshow(spectrum_hp, cmap="gray")
    plt.title("High-Pass Spectrum")
    plt.axis("off")

    # Single frequency result
    plt.subplot(2, 4, 7)
    plt.imshow(img_single_freq, cmap="gray")
    plt.title("Single Frequency Reconstruction")
    plt.axis("off")

    # Single frequency spectrum
    plt.subplot(2, 4, 8)
    plt.imshow(spectrum_single, cmap="gray")
    plt.title("Single Frequency Spectrum")
    plt.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
