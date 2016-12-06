

from hardware.MC1000_serial import mc1000
from hardware.serial_rs830 import rs830
from hardware.spectrometer import SP2300


import matplotlib.pylab as plt
import numpy as np

import time


# lockin.frequency = 150
#
chopper = mc1000()
chopper.frequency = 150


lockin = rs830()
# print(chopper.frequency)
mono = SP2300()

time.sleep(1)

for wavelength in np.arange(900, 1400, 100):
    print('here')
    mono.goto_nm(wavelength)
    time.sleep(5)
    print(mono.get_nm(), wavelength)
    # print(mono._is_mono_moving())
    plt.plot(mono.get_nm(), lockin.r, '.')
    plt.plot(mono.get_nm(), lockin.r, '.')
    plt.plot(mono.get_nm(), lockin.r, '.')

plt.semilogy()
plt.show()
