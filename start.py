#!/usr/bin/env python3

import kati.controller
import time
import logging

# start logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# init
controller = kati.controller.Controller()
log.info("started")

try:
    # main loop
    while True:
        time.sleep(300)
except (KeyboardInterrupt, SystemExit):
    # cleanup
    controller.shutdown()
    log.info("shutdown complete")
