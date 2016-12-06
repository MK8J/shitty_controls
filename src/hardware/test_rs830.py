

from MC1000_serial import mc1000
from rs830_serial import rs830
import matplotlib.pylab as plt
import time
import numpy as np

chopper = mc1000()
chopper.frequency = 163
# chopper.start

lockin = rs830()

# inital setting
lockin.frequency = 163
# lockin.input_configuration = 0
# lockin.input_shield_grounding = 0  # 0 float, 1 grounded
# lockin.input_coupling = 0  # 0 is AC 1 is DC
# lockin.filter_slope = 3  # 0 to 3, with 3 being more fitlering.
# lockin.reference_source = 0  # i selects  internal (i=1) or external (i=0).
lockin.sample_rate = 13
print(lockin.sample_rate)
time.sleep(1)
lockin.clear_data_store
print(lockin.start_data_store)
data = lockin.get_stored_points
lockin.clear_data_store

fig, ax = plt.subplots(1, 2)

for times in [10e-3, 1]:
    for freq in [50, 100, 163, 173]:
        lockin.time_constant = times
        lockin.frequency = freq
        # time.sleep(0.5)
        print(lockin.start_data_store)
        data = lockin.get_stored_points
        time.sleep(times * 1.5)
        lockin.clear_data_store
        ax[1].plot(freq, np.mean(data) / np.std(data), 'o', label=times)
        # ax[0].plot(lockin.r, 'o', label=freq)
        ax[0].plot(data, '.-', label=freq)
        # ax[0].plot(lockin.r, 'o', label=freq)
    # plt.plot(freq, np.mean(data), '^-')
lockin.stop_data_store
plt.title(lockin.time_constant)
ax[0].legend(loc=0)
ax[1].legend(loc=0)
lockin.close()
plt.show()
