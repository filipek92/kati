#!/usr/bin/env python3

import pigpio
import time
import logging
import kati.reader
import kati.kristin

# start logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def callback_indoor(num_bits, value):
    log.info("indoor: 0x%s", kati.kristin.format_card_number(value))


def callback_outdoor(num_bits, value):
    log.info("outdoor: 0x%s", kati.kristin.format_card_number(value))


# init GPI
pi = pigpio.pi()

# init readers
r_indoor = kati.reader.Reader(pi, 24, 10, 9, 25, 11, 8, 7, callback_indoor)
r_outdoor = kati.reader.Reader(pi, 12, 13, 19, 16, 26, 20, 21, callback_outdoor)

log.debug("started")

# main loop
try:
    while True:
        time.sleep(300)
except KeyboardInterrupt:
    pass

log.debug("shutdown")

# cleanup
r_indoor.cancel()
r_outdoor.cancel()
pi.stop()
