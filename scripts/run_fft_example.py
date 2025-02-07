import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2


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


def load_image_as_grayscale(path):
    """
    Loads an image from disk and converts it to a 2D NumPy array (grayscale).
    """
    img = Image.open(path).convert("L")
    return np.array(img)


def fft_image(image):
    """
    Compute the 2D FFT of the image and shift the DC component to the center.
    Returns the shifted FFT result.
    """
    F = np.fft.fft2(image)
    F_shifted = np.fft.fftshift(F)
    return F_shifted


def ifft_image(F_shifted):
    """
    Compute the inverse 2D FFT from the shifted frequency representation.
    """
    F_ishifted = np.fft.ifftshift(F_shifted)
    img_reconstructed = np.fft.ifft2(F_ishifted)
    return np.abs(img_reconstructed)


def low_pass_filter(F_shifted, cutoff):
    """
    Create a circular low-pass filter with a given cutoff radius.
    Zeroes out frequencies outside the cutoff.
    """
    rows, cols = F_shifted.shape
    crow, ccol = rows // 2, cols // 2

    # Create a mask with the same dimensions as the FFT
    mask = np.zeros_like(F_shifted)

    # We only keep frequencies within the cutoff distance from the center
    for r in range(rows):
        for c in range(cols):
            if (r - crow) ** 2 + (c - ccol) ** 2 < cutoff**2:
                mask[r, c] = 1

    # Apply the mask to the shifted FFT
    F_filtered = F_shifted * mask
    return F_filtered


def high_pass_filter(F_shifted, cutoff):
    """
    Create a circular high-pass filter with a given cutoff radius.
    Zeroes out frequencies below the cutoff.
    """
    rows, cols = F_shifted.shape
    crow, ccol = rows // 2, cols // 2

    # Create a mask with the same dimensions as the FFT
    mask = np.ones_like(F_shifted)

    # We zero out frequencies within the cutoff distance from the center
    for r in range(rows):
        for c in range(cols):
            if (r - crow) ** 2 + (c - ccol) ** 2 < cutoff**2:
                mask[r, c] = 0

    # Apply the mask to the shifted FFT
    F_filtered = F_shifted * mask
    return F_filtered


def select_single_frequency(F_shifted, freq_x, freq_y, band_radius=2):
    """
    Keep only a small neighborhood of frequencies around (freq_x, freq_y).
    freq_x, freq_y are offsets from the center in the frequency domain.

    band_radius: how many pixels around (freq_x, freq_y) we keep.
    The rest is set to zero.
    """
    rows, cols = F_shifted.shape
    crow, ccol = rows // 2, cols // 2

    # Create a mask of all zeros
    mask = np.zeros_like(F_shifted)

    # Coordinates in the frequency domain
    center_x = ccol + freq_x
    center_y = crow + freq_y

    # Keep values near (center_y, center_x) in a small square region
    row_min = max(center_y - band_radius, 0)
    row_max = min(center_y + band_radius + 1, rows)
    col_min = max(center_x - band_radius, 0)
    col_max = min(center_x + band_radius + 1, cols)

    mask[int(row_min) : int(row_max), int(col_min) : int(col_max)] = 1

    # Also keep the corresponding mirrored frequency (negative freq_x, freq_y)
    # Because real images typically have symmetric spectra
    mirror_x = ccol - freq_x
    mirror_y = crow - freq_y

    row_min_m = max(mirror_y - band_radius, 0)
    row_max_m = min(mirror_y + band_radius + 1, rows)
    col_min_m = max(mirror_x - band_radius, 0)
    col_max_m = min(mirror_x + band_radius + 1, cols)

    mask[int(row_min_m) : int(row_max_m), int(col_min_m) : int(col_max_m)] = 1
    # Apply the mask
    F_filtered = F_shifted * mask
    return F_filtered


def main():
    # ------------------------------------
    # 1) Load or create a test image
    # ------------------------------------

    # Option A: Use a synthetic gradient image
    # img = create_synthetic_gradient(width=256, height=256)
    # Option B: Load an actual image from diskimage = plt.imread('../imgs/image.png')  # Replace with your image path
    img = cv2.imread("imgs/image.png", 0)
    img = cv2.resize(img, (img.shape[1] // 10, img.shape[0] // 10))
    # img = load_image_as_grayscale("path_to_your_image.jpg")

    # ------------------------------------
    # 2) Compute the 2D FFT
    # ------------------------------------
    F_shifted = fft_image(img)

    # ------------------------------------
    # 3) Low-pass filter
    # ------------------------------------
    cutoff_radius_lp = 20
    F_low_pass = low_pass_filter(F_shifted, cutoff_radius_lp)
    img_lp = ifft_image(F_low_pass)

    # ------------------------------------
    # 4) High-pass filter
    # ------------------------------------
    cutoff_radius_hp = 20
    F_high_pass = high_pass_filter(F_shifted, cutoff_radius_hp)
    img_hp = ifft_image(F_high_pass)

    # ------------------------------------
    # 5) Single frequency selection
    #    Example: pick some small offset from center in x & y
    # ------------------------------------
    freq_x, freq_y = 10, 10  # Adjust as needed
    F_single_freq = select_single_frequency(F_shifted, freq_x, freq_y, band_radius=0)
    img_single_freq = ifft_image(F_single_freq)
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
