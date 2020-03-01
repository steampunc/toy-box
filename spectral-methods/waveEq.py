import numpy as np
import math
import matplotlib.pyplot as plt
import os

size = 256
dx = 2 * math.pi / size
dt = 0.001
maxT = 5
freqs = np.fft.fftfreq(size, dx);

def deriv(array, n):
    for i in range(array.shape[0]):
        der = (2 * math.pi * 1j * freqs[i])
        if not np.isclose(der, 0):
            array[i] = (der ** n) * array[i]


## SOLVING the wave eqn

# initial conditions
x = np.arange(size) * dx
f0 = np.sin(x)#np.exp(- (x - dx * size / 2) ** 2)
c = 1

# Analytical solution to problem
def real(time, f_n):
    f_t = np.sin(x - c * time)
    l2 = np.sqrt(np.absolute(((f_t - f_n)**2)))
    print(np.sum(l2))
    

# Find R_n through FFT
F_n = np.fft.fft(f0)
R_n = np.copy(F_n)
deriv(R_n, 1)
R_n = - c * R_n

F_nm1 = np.copy(F_n)


# Leapfrog to advance F
for i in range(0, int(maxT / dt)):
    print("Calculating time {0:.3f}".format(i * dt))
    R_n = np.copy(F_n)
    deriv(R_n, 1)
    R_n = - c * R_n

    F_ntemp = np.copy(F_n)
    F_n = F_nm1 + 2 * dt * R_n
    F_nm1 = F_ntemp

    # Inverting to see behavior
    if (i % 5 == 0):
        f_t = np.fft.ifft(F_n)
        real(dt * i, f_t)
        plt.plot(x, f0, 'C1', label='f0')
        plt.plot(x, f_t.real, 'C2', label='f_t')
        plt.show(block=False)
        plt.pause(0.05)
        plt.cla()



