#!/usr/bin/env python3

import pigpio
import logging
import kati.wiegand


BEEP_LEN = 2000 * 1000  # in microseconds
GREEN_BLINK_LEN = BEEP_LEN  # in microseconds


def _get_raspberry_serial_number():
    with open("/proc/cpuinfo") as cpuinfo:
        for line in cpuinfo:
            if "Serial" in line:
                return line.split(":")[-1].strip()


class Reader:
    """
    A class representing a physical card reader with all of its capabilities.
    """

    def __init__(self, pi, beeper, hold, data_0, data_1, led_green, led_red,
                 tamper, data_callback, tamper_callback=None, text_id=None):
        """
        Start Wiegand decoder, setup output ports, prepare waves and register callbacks.
        """
        self.pi = pi
        self.hold = hold
        self.led_red = led_red
        self.data_callback = data_callback

        if text_id:
            self.text_id = text_id
        else:
            # no explicit text_id provided - combine this Raspberry's serial
            # number with data_1 gpio (determines indoor/outdoor reader)
            self.text_id = "{}{}".format(_get_raspberry_serial_number(), data_1)

        # start logger
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger("{}(text_id={})".format(__name__, self.text_id))

        # start wiegand decoder with passed callback
        self.wiegand = kati.wiegand.decoder(pi, data_0, data_1, self._callback)

        # set output mode and clear values (HIGH = logical 0)
        for port in beeper, hold, led_green, led_red:
            pi.set_mode(port, pigpio.OUTPUT)
            pi.write(port, pigpio.HIGH)

        # prepare waves
        self._setup_beep_wave(beeper)
        self._setup_green_bink_wave(led_green)

        # handle tamper
        if tamper_callback:
            pi.set_mode(tamper, pigpio.INPUT)
            pi.set_pull_up_down(tamper, pigpio.PUD_UP)
            self.cb_tamper = pi.callback(tamper, pigpio.RISING_EDGE, tamper_callback)
        else:
            self.cb_tamper = None

    def _setup_beep_wave(self, beeper):
        # see http://abyz.co.uk/rpi/pigpio/python.html#wave_create
        wf = []
        wf.append(pigpio.pulse(0, 1 << beeper, BEEP_LEN))
        wf.append(pigpio.pulse(1 << beeper, 0, 0))

        self.pi.wave_add_new()
        self.pi.wave_add_generic(wf)
        self.beep_wave = self.pi.wave_create()  # create and save id
        assert self.beep_wave >= 0, "Unable to create beep wave"

    def _setup_green_bink_wave(self, led_green):
        wf = []
        wf.append(pigpio.pulse(0, 1 << led_green, GREEN_BLINK_LEN))
        wf.append(pigpio.pulse(1 << led_green, 0, 0))

        self.pi.wave_add_new()
        self.pi.wave_add_generic(wf)
        self.green_blink_wave = self.pi.wave_create()
        assert self.green_blink_wave >= 0, "Unable to create green blink wave"

    def _callback(self, num_bits, card_number):
        self.log.info("read %d bits, data %s", num_bits, card_number)
        self.data_callback(num_bits, card_number)

    def beep(self):
        """
        Start one time non-blocking beep.
        """
        self.pi.wave_send_once(self.beep_wave)
        self.log.info("beep for %.1f seconds", BEEP_LEN / 1e6)

    def green_blink(self):
        """
        Start one time non-blocking green LED blink.
        """
        self.pi.wave_send_once(self.green_blink_wave)
        self.log.info("green blink for %.1f seconds", GREEN_BLINK_LEN / 1e6)

    def cancel(self):
        """
        Release resources.
        """
        self.pi.wave_delete(self.beep_wave)
        self.pi.wave_delete(self.green_blink_wave)
        if self.cb_tamper:
            self.cb_tamper.cancel()


if __name__ == "__main__":
    # demo
    import time

    def callback(bits, value):
        print("bits={} value={}".format(bits, value))

    pi = pigpio.pi()
    r = Reader(pi, 24, 10, 9, 25, 11, 8, 7, callback)
    time.sleep(300)
    r.cancel()
    pi.stop()
