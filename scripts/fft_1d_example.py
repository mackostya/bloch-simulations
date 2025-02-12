import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams.update({"font.size": 22})


# Plot the original signal
def plot_signal(t, signal):
    plt.figure(figsize=(12, 6))
    plt.plot(t, signal, color="black")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("Measured Signal")
    # plt.legend()
    plt.grid()
    plt.show()


# Plot the estimated components
def plot_components(positive_freqs, amplitudes_cos_estimated, amplitudes_sin_estimated):
    plt.figure(figsize=(12, 6))
    plt.plot(positive_freqs[:100], amplitudes_cos_estimated[:100], "r", label="Estimated Cosine Components")
    plt.plot(positive_freqs[:100], amplitudes_sin_estimated[:100], "b", label="Estimated Sine Components")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.title("Estimated Signal Components")
    plt.legend()
    plt.grid()
    plt.show()


# Plot the individual cosine and sine components
def plot_individual_components(t, frequencies, amplitudes_cos, amplitudes_sin):
    plt.figure(figsize=(12, 6))
    for f, ac, as_ in zip(frequencies, amplitudes_cos, amplitudes_sin):
        component = ac * np.cos(2 * np.pi * f * t) + as_ * np.sin(2 * np.pi * f * t)
        plt.plot(t, component, label=f"Component {f} Hz")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("Individual Components")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":

    # Parameters
    sampling_rate = 1000  # Hz
    T = 1.0  # seconds
    N = int(sampling_rate * T)  # number of samples
    t = np.linspace(0, T, int(N), endpoint=False)  # time vector

    # Create a signal as a sum of cosine and sine functions
    frequencies = [5, 15, 30]  # Hz
    amplitudes_cos = [3, 2, 1]
    amplitudes_sin = [1, 2, 3]
    signal = sum(
        ac * np.cos(2 * np.pi * f * t) + as_ * np.sin(2 * np.pi * f * t)
        for f, ac, as_ in zip(frequencies, amplitudes_cos, amplitudes_sin)
    )

    # Compute FFT
    fft_values = np.fft.fft(signal)
    frequencies_fft = np.fft.fftfreq(int(N), d=1 / sampling_rate)  # Frequency bins

    # Extract positive frequencies
    positive_freqs = frequencies_fft[: N // 2]
    amplitudes_cos_estimated = 2 * np.real(fft_values[: N // 2]) / N
    amplitudes_sin_estimated = -2 * np.imag(fft_values[: N // 2]) / N

    # Run the plots
    plot_signal(t, signal)
    plot_components(positive_freqs, amplitudes_cos_estimated, amplitudes_sin_estimated)
    plot_individual_components(t, frequencies, amplitudes_cos, amplitudes_sin)
