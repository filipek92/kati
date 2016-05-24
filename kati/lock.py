#!/usr/bin/env python3

import pigpio
import logging


HOLD_LEN = 2000 * 1000  # in microseconds


# start logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Lock:
    """
    A class representing a physical lock.
    """

    def __init__(self, pi, port):
        """
        Setup output ports and prepare waves.
        """
        self.pi = pi

        # setup output
        pi.set_mode(port, pigpio.OUTPUT)
        pi.write(port, pigpio.HIGH)

        # prepare waves
        # see http://abyz.co.uk/rpi/pigpio/python.html#wave_create
        wf = []
        wf.append(pigpio.pulse(0, 1 << port, HOLD_LEN))
        wf.append(pigpio.pulse(1 << port, 0, 0))

        self.pi.wave_add_new()
        self.pi.wave_add_generic(wf)
        self.wave = self.pi.wave_create()  # create and save id
        assert self.wave >= 0, "Unable to create lock wave"

    def unlock(self):
        """
        Hold a lock for a while (non-blocking).
        """
        self.pi.wave_send_once(self.wave)
        log.info("unlock for %.1f seconds", HOLD_LEN / 1e6)

    def cancel(self):
        """
        Release resources.
        """
        self.pi.wave_delete(self.wave)


if __name__ == "__main__":
    # demo
    import time

    pi = pigpio.pi()
    l = Lock(pi, 17)

    for i in range(10):
        l.unlock()
        time.sleep(10)

    l.cancel()
    pi.stop()
