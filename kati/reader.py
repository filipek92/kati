#!/usr/bin/env python3

import pigpio
import wiegand


BEEP_LENGTH = 1e6  # in microseconds


class Reader:
    """
    A class representing a physical card reader with all of its capabilities.
    """

    def __init__(self, pi, beeper, hold, data_0, data_1, led_green, led_red,
                 tamper, data_callback, tamper_callback=None):
        """
        Start Wiegand decoder, setup output ports, prepare waves and register callbacks.
        """
        self.pi = pi
        # self.hold = hold
        # self.led_green = led_green
        # self.led_red = led_red

        # start wiegand decoder with passed callback
        self.wiegand = wiegand.decoder(pi, data_0, data_1, data_callback)

        # set outputs
        pi.set_mode(beeper, pigpio.OUTPUT)
        pi.set_mode(hold, pigpio.OUTPUT)
        pi.set_mode(led_green, pigpio.OUTPUT)
        pi.set_mode(led_red, pigpio.OUTPUT)

        # prepare waves
        self._setup_beep_wave(beeper)

        # handle tamper
        # if tamper_callback:
        #     pi.set_mode(tamper, pigpio.INPUT)
        #     pi.set_pull_up_down(tamper, pigpio.PUD_UP)
        #     self.cb_tamper = pi.callback(tamper, pigpio.RISING_EDGE, tamper_callback)
        # else:
        #     self.cb_tamper = None

    def _setup_beep_wave(self, beeper):
        # see http://abyz.co.uk/rpi/pigpio/python.html#wave_create
        wf = []
        wf.append(pigpio.pulse(1 << beeper, 0, BEEP_LENGTH))
        wf.append(pigpio.pulse(0, 1 << beeper, 0))

        self.pi.wave_add_new()
        self.pi.wave_add_generic(wf)
        self.beep_wave = self.pi.wave_create()  # create and save id
        assert self.beep_wave >= 0, "Unable to create wave"

    def beep(self):
        """
        Start one time non-blocking beep.
        """
        self.pi.wave_send_once(self.beep_wave)

    def cancel(self):
        """
        Release resources.
        """
        self.pi.wave_delete(self.beep_wave)
        if self.cb_tamper:
            self.cb_tamper.cancel()


if __name__ == "__main__":
    # demo
    import time

    def callback(bits, value):
        print("bits={} value={}".format(bits, value))

    pi = pigpio.pi()
    r = Reader(pi, 18, 19, 21, 22, 23, 24, 26, callback)
    time.sleep(300)
    r.cancel()
    pi.stop()