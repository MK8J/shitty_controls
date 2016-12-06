import serial
import time


def _ask_for_values(obj, string, reads=1):
    obj.write(str.encode(string + '\r'))
    s = b''
    for i in range(reads):
        s += obj.readline()
        s = s.decode("utf-8")

    return s


class SP2300():

    def __init__(self):
        # self.m=instrument(get_instruments_list()[0])
        # try:
        # open first serial port
        self.m = serial.Serial('COM4', 9600, timeout=1)
        # except:
        # print "Check if monochromotor is connected to right COM port of
        # instrument list (see control panel, hardward devices). Cannot connect
        # to monochromator. Check connection. Check drivers"
        if self.m.isOpen():
            print('open')

    def close(self):
        self.m.close()

    def get_nm(self):
        self.curr_nm = _ask_for_values(self.m, '?NM')
        try:
            val = float(self.curr_nm.strip(' nm  ok\r\n'))
        except:
            # print(self.curr_nm)
            val = 5
        return val

    def get_nm_per_min(self):
        self.curr_nm_min = _ask_for_values(self.m, '?NM/MIN')
        return self.curr_nm_min

    def get_serial_model(self):
        self.serial_no = _ask_for_values(self.m, 'SERIAL')
        self.model_no = _ask_for_values(self.m, 'MODEL')
        return self.serial_no, self.model_no

    def goto_nm_max_speed(self, nm):
        self.m.ask('%0.2f GOTO' % nm)

    def get_turret(self):
        self.turret = _ask_for_values(self.m, '?TURRET')
        return self.turret

    def get_mirror(self):
        self.mirror = _ask_for_values(self.m, '?TURRET')
        return self.mirror

    def get_filter(self):
        self.filter = _ask_for_values(self.m, '?FILTER')
        return self.filter

    def get_grating(self):
        self.grating = _ask_for_values(self.m, '?GRATING')
        return self.grating

    def get_gratings(self):
        self.gratings = _ask_for_values(self.m, '?GRATINGS', 11)
        return self.gratings

    def set_turret(self, num):
        if num <= 2:
            self.m.ask(str(int(num)) + ' TURRET')
        else:
            print("There is not turret with this input")

    def set_filter(self, num):
        if num <= 6:
            self.m.ask(str(int(num)) + ' FILTER')
            print("Filter changed and waiting with additional delay...")
            time.sleep(1)  # Additional delay, just in case.
            print("Done waiting")
        else:
            print("There is no filter with this input")

    def set_grating(self, num):
        if num <= 2:
            self.m.ask(str(int(num)) + ' GRATING')
            # time.sleep(5) # Additional delay, just in case
        else:
            print("There is no grating with this input")

    def goto_nm_with_set_nm_per_min(self, nm, nm_per_min):
        self.m.ask('%0.2f NM/MIN' % nm_per_min)
        self.m.ask('%0.2f >NM' % nm)
        char = 0
        while char != 1:
            s = self.m.ask('MONO-?DONE')
            char = int(s[2])
            # print "Current wavelength is "+ self.m.ask('?NM')
            time.sleep(.2)
        print("Scan done?: " + 'yes' if char == 1 else 'No')
        self.m.ask('MONO-STOP')
        return _ask_for_values(self.m, '?NM')

    def _is_mono_moving(self):
        '''
        Checks and loops until the monochromator is finished moving
        '''
        value = False
        while value is False:
            value = b' 1  ok\r\n' == _ask_for_values(self.m, 'MONO-?DONE')
        return False

    def goto_nm(self, nm):

        val = _ask_for_values(self.m, '{0:0.3f} GOTO'.format(nm), 1)
        # print(val)
        # time.sleep(2)
        # self._is_mono_moving()
        # self.m.ask('%0.2f >NM' % nm)
        # char = 0
        # while char != 1:
        #     s = self.m.ask('MONO-?DONE')
        #     char = int(s[2])
        #     # print "Current wavelength is "+ self.m.ask('?NM')
        #     time.sleep(.2)
        # print("Scan done?: " + 'yes' if char == 1 else 'No')
        # self.m.ask('MONO-STOP')
        return self.get_nm()

if __name__ == "__main__":
    # This part of the codes uses the SP2300 class to do a wavelength scan
    a = SP2300()
    print(a.get_serial_model())
    print(a.get_grating())
    print(a.get_filter())
    print(a.get_nm_per_min())
    print(a.get_nm())
    # print(a.goto_nm_with_set_nm_per_min())
    print(a.get_mirror())
    print(a.get_gratings())
    # print(a._is_mono_moving())
    print(a.goto_nm(300))
    print(a.close())

    # a.set_grating(2) # can only take 1 or 2 as input
    #
    # start_wave=500
    # end_wave=1000
    # delta_wave=20
    # speed_nm_per_min=2000
    # a.set_filter(2) # this applies the 320 nm filter in the beginning
    # for i in xrange(start_wave,end_wave,delta_wave):
    # print "----------------------------"
    # print "Wavelength input is %0.2f nm" % i
    # wave=a.goto_nm_with_set_nm_per_min(i,speed_nm_per_min)
    #
    # if i <= 370 and i+delta_wave >= 370:
    #   a.set_filter(2)
    #
    # if i <= 660 and i+delta_wave >= 660:
    #   a.set_filter(3)
    #
    # if i <= 775 and i+delta_wave >= 775:
    #   a.set_filter(4)
    #
    # if i <= 1300 and i+delta_wave >= 1300:
    #   a.set_filter(5)
    #
    # print "Wavelength output is "+str(wave[0])+ " nm"
    # print "----------------------------"
    #
    # print "Resetting the monochromator to home position"
    # a.goto_nm_max_speed(400)
    # a.set_filter(1)
    # print "Position to home at  " + str(a.get_nm()[0]) + " nm"+ ' and filter has been reset to ' + str(a.get_filter()[0])
    # print "Monochromator scan done. Have a nice day!"
