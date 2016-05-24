#!/usr/bin/env python3

import pigpio
import time
import logging
import kati.reader
import kati.lock
import kati.kristin


# start logger
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class Kati(object):

    def __init__(self, pi):
        self.pi = pi

        # init physical components
        self.lock = kati.lock.Lock(pi, 17)
        self.reader_indoor = kati.reader.Reader(pi, 24, 10, 9, 25, 11, 8, 7, self._callback_indoor)
        self.reader_outdoor = kati.reader.Reader(pi, 12, 13, 19, 16, 26, 20, 21, self._callback_outdoor)

    def _callback(self, the_reader, card_number):
        # TODO handle timeout
        # TODO use the_reader.text_id as reader ID
        if kati.kristin.has_access(1, card_number):
            # if user has access, unlock
            log.info("access granted")
            self.lock.unlock()
            # TODO cannot send multiple waveforms, need to merge
            # the_reader.green_blink()
        else:
            # otherwise beep
            log.info("access denied")
            the_reader.beep()

    def _callback_indoor(self, num_bits, card_number):
        self._callback(self.reader_indoor, card_number)

    def _callback_outdoor(self, num_bits, card_number):
        self._callback(self.reader_outdoor, card_number)

    def cancel(self):
        self.reader_indoor.cancel()
        self.reader_outdoor.cancel()
        self.lock.cancel()


# init
pi = pigpio.pi()
k = Kati(pi)
log.debug("started")

# main loop
try:
    while True:
        time.sleep(300)
except KeyboardInterrupt:
    pass

# cleanup
log.debug("shutdown")
k.cancel()
pi.stop()
