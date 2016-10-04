#!/usr/bin/env python3

import kati.controller
import time
import logging
import signal

stop = False


def shutdown(signum, frame):
    global stop
    stop = True

# register shutdown handler
signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)


# start logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# init controller
controller = kati.controller.Controller()
log.info("started")


try:
    while not stop:
        time.sleep(1)
finally:
    controller.shutdown()
    log.info("shutdown complete")
