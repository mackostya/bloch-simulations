import numpy as np

# ----------------------------
# FFT / IFFT Helper Functions
# ----------------------------
def fft_image(image):
    F = np.fft.fft2(image)
    F_shifted = np.fft.fftshift(F)
    return F_shifted

def ifft_image(F_shifted):
    F_ishifted = np.fft.ifftshift(F_shifted)
    img_reconstructed = np.fft.ifft2(F_ishifted)
    return np.abs(img_reconstructed)

# ----------------------------
# Filters
# ----------------------------
def low_pass_filter(F_shifted, cutoff):
    """
    Circular low-pass filter with radius = cutoff.
    Zeros out everything beyond cutoff distance from center.
    """
    rows, cols = F_shifted.shape
    crow, ccol = rows // 2, cols // 2

    # Create a boolean mask
    Y, X = np.ogrid[:rows, :cols]
    dist_sq = (Y - crow)**2 + (X - ccol)**2
    mask = dist_sq <= cutoff**2
    
    return F_shifted * mask

def high_pass_filter(F_shifted, cutoff):
    """
    Circular high-pass filter with radius = cutoff.
    Zeros out everything within cutoff distance from center.
    """
    rows, cols = F_shifted.shape
    crow, ccol = rows // 2, cols // 2

    # Create a boolean mask
    Y, X = np.ogrid[:rows, :cols]
    dist_sq = (Y - crow)**2 + (X - ccol)**2
    mask = dist_sq > cutoff**2
    
    return F_shifted * mask

def select_single_frequency(F_shifted, freq_x, freq_y, band_radius):
    """
    Retains only a small region (band_radius in each direction)
    around (freq_x, freq_y) and its mirrored location. 
    Everything else is zeroed out.
    """
    rows, cols = F_shifted.shape
    crow, ccol = rows // 2, cols // 2

    # Create a boolean mask (all False initially)
    mask = np.zeros_like(F_shifted, dtype=bool)
    
    # Primary frequency
    cx = int(ccol + freq_x)
    cy = int(crow + freq_y)
    
    # Bounds for primary
    row_min = max(cy, 0)
    row_max = min(cy + band_radius, rows)
    col_min = max(cx, 0)
    col_max = min(cx + band_radius, cols)
    
    mask[row_min:row_max, col_min:col_max] = True

    # Mirrored frequency
    mx = int(ccol - freq_x)
    my = int(crow - freq_y)
    
    # Bounds for mirror
    row_min_m = max(my, 0)
    row_max_m = min(my + band_radius, rows)
    col_min_m = max(mx, 0)
    col_max_m = min(mx + band_radius, cols)
    
    mask[row_min_m:row_max_m, col_min_m:col_max_m] = True

    return F_shifted * mask