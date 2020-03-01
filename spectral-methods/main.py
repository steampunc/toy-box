# I know I gave up on the C++ fftw linking stuff, just cut me some slack ugh :P

import numpy as np
import math
import matplotlib.pyplot as plt
import os


fileIndex = 0
while os.path.exists("logs/f_t%s.csv" % fileIndex):
    fileIndex += 1

size = 32
dx = 2 * math.pi / size
dt = 0.005
maxT = 5
freqs = np.fft.fftfreq(size, dx);

def deriv(array, n):
    for i in range(array.shape[0]):
        der = (2 * math.pi * 1j * freqs[i])
        if not np.isclose(der, 0):
            array[i] = (der ** n) * array[i]


## SOLVING poisson's eqn

# initial conditions
x = np.arange(size) * dx
f0 = np.sin(x)
sigma = 0.5

# Analytical solution to calculate L2 norm
def real(time, f_n):
    f_t = math.exp(- time * sigma) * f0
    l2 = np.sqrt(np.absolute(((f_t - f_n)**2)))
    print(np.sum(l2))

# Find R_n through FFT
F_n = np.fft.fft(f0)
R_n = np.copy(F_n)
deriv(R_n, 2)
R_n = sigma * R_n
R_nm1 = np.copy(R_n)

# Adams-Bashforth to advance F
for i in range(0, int(maxT / dt)):
    print("Calculating time {0:.3f}".format(i * dt))
    R_n = np.copy(F_n)
    deriv(R_n, 2)
    R_n = sigma * R_n

    F_n = F_n + (dt / 2) * (3 * R_n - R_nm1)

    R_nm1 = np.copy(R_n)

    # Inverting to see behavior
    if (i % 5 == 0):
        f_t = np.fft.ifft(F_n)
        real(i * dt, f_t)
        plt.plot(x, f0, 'C1', label='f0')
        plt.plot(x, f_t.real, 'C2', label='f_t')
        plt.show(block=False)
        plt.pause(0.05)
        plt.cla()



