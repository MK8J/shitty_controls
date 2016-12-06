import serial
import time
# a = serial.Serial('COM6', 19200, timeout=1)
# a.write(b'R\n')
# print(a.readline())
# # a.write(b'B 0\n')
# # print(a.readline())
#
# a.write(b'I 80\n')
# print(a.readline())
# a.write(b'E\n')
# print(a.readline())
# print(a.readline())
# print(a.readline())
# print(a.readline())
# print(a.readline())
# print(a.readline())
# a.close()
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

#


def _ask_for_values(obj, string, reads=1):
    print(str.encode(string))
    for i in string:
        obj.write(str.encode(i))
        # print(obj.readline())
        time.sleep(0.1)
    s = b''
    for i in range(reads):
        s += obj.readline()
    return s.decode()


class mc1000():

    def __init__(self):

        self.inst = serial.Serial(
            'COM6', 19200, timeout=0.1, parity=serial.PARITY_NONE)
        self.inst.reset_input_buffer()
        self.inst.reset_output_buffer()
        if self.inst.isOpen():
            print('open')

        print(self.inst.readlines())

    def close(self):
        self.inst.close()

    @property
    def start(self):
        '''
        queries the input line notch filter
        '''
        return _ask_for_values(self.inst, 'R', 0)

    @property
    def frequency(self):
        '''
        queries the input line notch filter
        '''
        # print(_ask_for_values(self.inst, 'I', 5))
        # print(self.inst.readline())
        # print(self.inst.readline())
        # print(_ask_for_values(self.inst, '40', 5))
        # return _ask_for_values(self.inst, 'I', 5)
        return 5

    @frequency.setter
    def frequency(self, value):
        '''
        queries the input line notch filter
        '''

        self.inst.reset_input_buffer()

        _ask_for_values(self.inst, 'I{0:d}'.format(value))
        self.inst.write(b'\n')

        self.inst.reset_input_buffer()

    @property
    def chopper(self):
        print(_ask_for_values(self.inst, 'B0', 1))
        pass


if __name__ == '__main__':
    a = mc1000()
    # a.chopper
    print(a.start)

    # a.frequency = 133
    # a.start
    a.close()
#
