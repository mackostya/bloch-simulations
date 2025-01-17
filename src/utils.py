import numpy as np
from scipy.spatial.transform import Rotation as R


def abprop(*args):
    """
    This function is a python implementation of the MATLAB function:
    https://github.com/mribri999/MRSignalsSeqs/blob/master/Matlab/abprop.m
    """
    a_or_b = "a"
    A = np.eye(3)
    B = np.zeros((3, 1))
    A_prev = np.eye(3)
    for a in args:
        if a.shape == (3, 3):
            A = a @ A
            A_prev = a
            a_or_b = "a"
        elif a.shape == (3, 1) or a.shape == (3,):
            a = a.reshape(3, 1)
            if a_or_b == "a":
                B = A_prev @ B + a
                a_or_b = "b"
            else:
                raise ValueError("Invalid input, B is followed by another B")
    Mss = np.linalg.inv(np.eye(3) - A) @ B
    return A, B, Mss


def rot_x(angle):
    return R.from_euler("x", angle, degrees=True).as_matrix()


def rot_y(angle):
    return R.from_euler("y", angle, degrees=True).as_matrix()


def rot_z(angle):
    return R.from_euler("z", angle, degrees=True).as_matrix()


def mr2mc(Mr):
    Mc = np.zeros((len(Mr), 3), dtype=complex)
    Mc[:, 0] = Mr[:, 0] + 1j * Mr[:, 1]
    Mc[:, 1] = Mr[:, 0] - 1j * Mr[:, 1]
    Mc[:, 2] = Mr[:, 2]
    return Mc


def mc2mr(Mc):
    Mr = np.zeros((len(Mc), 3))
    Mr[:, 0] = np.real(Mc[:, 0])
    Mr[:, 1] = np.imag(Mc[:, 0])
    Mr[:, 2] = np.real(Mc[:, 2])  # actually the imaginary part should be zero
    return Mr


def msinc(N, ncyc):
    """
    Computes the sinc function modulated by a Hamming window.
    See MATLAB implementatino: https://github.com/mribri999/MRSignalsSeqs/blob/master/Matlab/msinc.m
    Parameters:
        N (int): Number of points.
        ncyc (int): Number of cycles.

    Returns:
        np.ndarray: The sinc function modulated by a Hamming window.
    """
    x = (((np.arange(N) + 0.5) - (N / 2 - 0.5)) / N) * 2 * ncyc
    hw = np.hamming(N)

    h = np.sinc(x) * hw

    return h
