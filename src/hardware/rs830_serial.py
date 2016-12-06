import serial
import time
import sys
import numpy as np
# a = serial.Serial('COM5', 9600, timeout=1)
# a.write(b'*IDN?\n')
# print(a.readline())
#
# a.write(b'OUTP? 1\n')
# print(a.readline())
#
# a.close()
# configure the lockin amplifier
# lockin.reserve = 'high'
# lockin.time_constant = 3
# # take 60 measurements and print the result
# for i in range(60):
#     print lockin.x
#     time.sleep(1)


def _ask_for_values(obj, string, reads=1):
    obj.write(str.encode(string + '\r'))
    s = b''
    for i in range(reads):
        s += obj.readline()
    return s


def _ask_for_values_with_check(obj, string, value, possible_values, reads=1):
    '''
    object: macine instance
    string: string to be sent, this includes the value to be sent
    reads: number of read listeners
    value: value to be send
    possible_values: a list of values that the value should be in
    '''
    if value in possible_values:
        value = _ask_for_values(obj, string, reads=1)
    else:
        print('Incorrected input try:', possible_values)
        value = 0
    return 0


def _ask_for_values_with_check_continious(obj, string, value, possible_values, reads=1):
    '''
    object: macine instance
    string: string to be sent, this includes the value to be sent
    reads: number of read listeners
    value: value to be send
    possible_values: a list of values that the value should be in
    '''
    if value >= possible_values[0] and value <= possible_values[1]:
        value = _ask_for_values(obj, string, reads=1)
    else:
        print('Incorrected value, must in in range:', possible_values)
        value = 0
    return 0


class rs830():

    interface_out = {'GPIB': '1',
                     'RS232': '0'
                     }

    _remotateacces = {'local': '0',
                      'remote': '1',
                      'lock out': '2',
                      }

    _sensitivity = {
        '2 nV/fA': '0',
        '5 nV/fA': '1',
        '10 nV/fA': '2',
        '20 nV/fA': '3',
        '50 nV/fA': '4',
        '100 nV/fA': '5',
        '200 nV/fA': '6',
        '500 nV/fA': '7',
        '1 uV/pA': '8',
        '2 uV/pA': '9',
        '5 uV/pA': '10',
        '10 uV/pA': '11',
        '20 uV/pA': '12',
        '50 uV/pA': '13',
        '100 uV/pA': '14',
        '200 uV/pA': '15',
        '500 uV/pA': '16',
        '1 mV/nA': '17',
        '2 mV/nA': '18',
        '5 mV/nA': '19',
        '10 mV/nA': '20',
        '20 mV/nA': '21',
        '50 mV/nA': '22',
        '100 mV/nA': '23',
        '200 mV/nA': '24',
        '500 mV/nA': '25',
        '1 V/uA': '26',
    }

    _time_constant = {10e-6: '0',
                      30e-6: '1',
                      100e-6: '2',
                      300e-6: '3',
                      1e-3: '4',
                      3e-3: '5',
                      10e-3: '6',
                      30e-3: '7',
                      100e-3: '8',
                      300e-3: '9',
                      1: '10',
                      3: '11',
                      10: '12',
                      30: '13',
                      100: '14',
                      300: '15',
                      1e3: '16',
                      3e3: '17',
                      10e3: '18',
                      30e3: '19'
                      }

    def __init__(self, port='COM5', interface='RS232'):

        self.inst = serial.Serial('COM5', 9600, timeout=0.1)

        self._setup(interface)

        if self.inst.isOpen():
            print('open')

    def close(self):
        self.inst.close()

    def _setup(self, interface):

        _ask_for_values(self.inst, 'LOCL ' +
                        self._remotateacces['remote'], 1)
        _ask_for_values(self.inst, 'OUTX ' +
                        self.interface_out[interface], 1)

    @property
    def sensitivity(self):
        return _ask_for_values(self.inst, 'SENS?', 1)

    @sensitivity.setter
    def sensitivity(self, value):
        if value in self._sensitivity.keys():
            _ask_for_values(self.inst, 'SENS ' + value, 1)
        else:
            print(value, ' not an accepted value, try', self._sensitivity.keys())
        pass

    @property
    def time_constant(self):
        return _ask_for_values(self.inst, 'OFLT?', 1)

    @time_constant.setter
    def time_constant(self, value):

        return _ask_for_values_with_check(self.inst,
                                          'OFLT {0}\n'.format(value),
                                          value,
                                          self._time_constant.keys())

    @property
    def idn(self):
        _ask_for_values(self.inst, '*IDN?', 1)
        return self.serial_no

    @property
    def x(self):
        '''
        Reads the value of x.
        '''
        return _ask_for_values(self.inst, 'OUTP? 1\n')

    @property
    def y(self):
        '''
        Reads the value of y.
        '''
        return _ask_for_values(self.inst, 'OUTP? 2\n')

    @property
    def r(self):
        '''
        Reads the value of r.
        '''
        return float(_ask_for_values(self.inst, 'OUTP? 3\n').decode("utf-8"))

    @property
    def theta(self):
        '''
        Reads the value of theta.
        '''
        return _ask_for_values(self.inst, 'OUTP? 4\n')

    @property
    def ch1(self):
        '''
        Reads the value of channel 1.
        '''
        return _ask_for_values(self.inst, 'OUTR? 1\n')

    @property
    def ch2(self):
        '''
        Reads the value of channel 2.
        '''
        return _ask_for_values(self.inst, 'OUTR? 2\n')

    @property
    def datapoints(self):
        '''
        Queries the number of data points stored in the internal buffer.
        '''
        return _ask_for_values(self.inst, 'SPTS?\n')

    @property
    def input_configuration(self):
        '''
        Quries the input confiuration
        '''
        return _ask_for_values(self.inst, 'ISRC?\n')

    @input_configuration.setter
    def input_configuration(self, value):
        '''
        Sets the input configuration
        '''
        #  The parameter
        # i selects A (i=0), A-B (i=1), I (1 MΩ) (i=2) or I (100 MΩ) (i=3)
        values = [0, 1, 2, 3]
        return _ask_for_values_with_check(self.inst,
                                          'ISRC {0}\n'.format(value),
                                          value,
                                          values)

    @property
    def reference_source(self):
        '''
        Quries the input confiuration
        '''
        return _ask_for_values(self.inst, 'FMOD?\n')

    @reference_source.setter
    def reference_source(self, value):
        '''
        Sets the input configuration
        '''
        #  The parameter
        # i selects internal (i=1) or external (i=0).
        values = [0, 1]
        return _ask_for_values_with_check(self.inst,
                                          'FMOD {0}\n'.format(value),
                                          value,
                                          values)

    @property
    def input_shield_grounding(self):
        '''
        queries the input shield grounding
        '''
        return _ask_for_values(self.inst, 'IGND?\n')

    @input_shield_grounding.setter
    def input_shield_grounding(self, value):
        '''
        sets the input shield grounding
        '''
        values = [0, 1]  # float, grounded
        return _ask_for_values_with_check(self.inst,
                                          'IGND {0}\n'.format(value),
                                          value,
                                          values)

    @property
    def filter_slope(self):
        '''
        queries the input coupling
        '''
        return _ask_for_values(self.inst, 'OFSL?\n')

    @filter_slope.setter
    def filter_slope(self, value):
        '''
        sets the input coupling
        '''
        values = [0, 1, 2, 3]
        # The parameter i selects 6 dB/oct (i=0), 12 dB/oct (i=1), 18 dB/oct
        # (i=2) or 24 dB/oct (i=3).
        return _ask_for_values_with_check(self.inst,
                                          'OFSL {0}\n'.format(value),
                                          value,
                                          values)

    @property
    def input_coupling(self):
        '''
        queries the input coupling
        '''
        return _ask_for_values(self.inst, 'ICPL?\n')

    @input_coupling.setter
    def input_coupling(self, value):
        '''
        sets the input coupling
        '''
        values = [0, 1]  # AC DC
        return _ask_for_values_with_check(self.inst,
                                          'ICPL {0}\n'.format(value),
                                          value,
                                          values)

    @property
    def input_line_notch_filter(self):
        '''
        queries the input line notch filter
        '''
        return _ask_for_values(self.inst, 'ILIN?\n')

    @input_line_notch_filter.setter
    def input_line_notch_filter(self, value):
        '''
        queries the input line notch filter
        '''
        values = [0, 1, 2, 3]  # no filters, Line notch in,   2xLine
        # notch in,  Both notch filters
        return _ask_for_values_with_check(self.inst,
                                          'ILIN {0}\n'.format(value),
                                          value,
                                          values)

    @property
    def frequency(self):
        '''
        queries the input line notch filter
        '''
        return float(_ask_for_values(self.inst, 'FREQ?\n'))

    @frequency.setter
    def frequency(self, value):
        '''
        queries the input line notch filter
        '''
        values = [0.001, 102000.]  # no filters, Line notch in,   2xLine
        # notch in,  Both notch filters
        return _ask_for_values_with_check_continious(self.inst,
                                                     'FREQ {0}\n'.format(
                                                         value),
                                                     value,
                                                     values)

    @property
    def sample_rate(self):
        '''
        queries queries the data sample rate.

        Generally, the highest possible sample rate should be used given the
        desired storage time. The lock-in time
        constant and filter slope should be chosen to attenuate signals at
        frequencies higher than 1/2 the sample rate
        as much as possible.

        '''
        print(_ask_for_values(self.inst, 'SRAT?\n', 10))
        print()
        return float(_ask_for_values(self.inst, 'SRAT?\n'))

    @sample_rate.setter
    def sample_rate(self, value):
        '''
        sets the data sample rate.

        '''
        values = [1, 2, 3,
                  4,
                  6,
                  5,
                  8,
                  7,
                  9,
                  10,
                  11,
                  12,
                  13,
                  14]
        return _ask_for_values_with_check(obj=self.inst,
                                          string='SRAT {0}\n'.format(value),
                                          value=value,
                                          possible_values=values,
                                          reads=1)

        # obj, string, value, possible_values, reads=1

    @property
    def no_stored_data_points(self):
        '''
        queries the number of data points stored. 16383 can be taken
        '''
        return float(_ask_for_values(self.inst, 'SPTS?\n', 1))

    @property
    def start_data_store(self):
        '''
        queries the number of data points stored.
        '''
        return _ask_for_values(self.inst, 'STRT\n')

    @property
    def stop_data_store(self):
        '''
        queries the number of data points stored.
        '''
        return _ask_for_values(self.inst, 'PAUS\n')

    @property
    def clear_data_store(self):
        '''
        queries the number of data points stored.
        '''
        return _ask_for_values(self.inst, 'REST\n')

    @property
    def get_stored_points(self):
        n = self.no_stored_data_points

        string = _ask_for_values(
            self.inst, 'TRCB ? 1,0,{0}\n'.format(n), 1)
        while (sys.getsizeof(string) - 1) % 4 != 0:
            print((sys.getsizeof(string) - 1) % 4, sys.getsizeof(string))
            string = _ask_for_values(
                self.inst, 'TRCB ? 1,0,{0}\n'.format(n), 1)

        print('done', (sys.getsizeof(string) - 1) % 4, sys.getsizeof(string))
        array = np.fromstring(string, dtype='<f4')

        return array


def freq_scan():
    import numpy as np
    for freq in np.arange(130, 140, 3):
        a.frequency = freq
        for i in range(10):
            # time.sleep(0.01)
            plt.plot(float(a.frequency),
                     float(a.r), '.')
            print('r:', a.r, a.frequency)

if __name__ == '__main__':

    import matplotlib.pylab as plt

    a = rs830(interface='RS232')
    a.sample_rate = '12'
    print(a.sample_rate)
    print(a.no_stored_data_points)
    # print(a.start_data_store)
    time.sleep(1)
    print(a.stop_data_store)
    print(a.no_stored_data_points)
    vals = a.get_stored_points

    plt.plot(vals)
    plt.show()
    # import time
    # import matplotlib.pylab as plt
    # freq_scan()
    # a.frequency = 133
    print('x:', a.x)
    # print('y:', a.y)
    # print('r:', a.r)
    # print('theta:', a.theta)
    # print('ch1:', a.ch1)
    # print('ch2:', a.ch2)
    # print('datapoints:', a.datapoints)
    # print('frequency:', a.frequency)
    # a.input_coupling = 1
    # a.input_configuration = 0

    a.close()
    # plt.show()
