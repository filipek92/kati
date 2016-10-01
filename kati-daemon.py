#!/usr/bin/env python3

import kati.controller
import time
import logging
import logging.handlers
import daemon

# start logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
syslog_handler = logging.handlers.SysLogHandler(address="/dev/log")
log.addHandler(syslog_handler)

# daemonize
with daemon.DaemonContext(files_preserve=[syslog_handler.socket.fileno()]):

    # init
    controller = kati.controller.Controller()
    log.info("kati controller started")

    try:
        # main loop
        while True:
            time.sleep(300)
    except (KeyboardInterrupt, SystemExit):
        # cleanup
        controller.shutdown()
        log.info("kati controller shutdown complete")
