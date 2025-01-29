import time
import sys
import getpass
import logging
import os
import platform

# to prevent error
logging.basicConfig()

# Singleton object
logger = logging.getLogger("shika")
logger.setLevel(logging.DEBUG)

debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception
log = logger.log


def config(beamline):
    logging.root.handlers = [] # clear basic config

    if beamline is None:
        beamline = "other"

    date = time.strftime("%Y%m%d")
    hostname = platform.node()
    hostname = hostname[:hostname.find(".")]
    username = getpass.getuser()
    pid = os.getpid()

    logfile = os.path.join("/isilon/cluster/log/shika/", beamline, "%s_%s.log"%(date, getpass.getuser()))
    formatf = "%(asctime)-15s " + " %s : %s : %d : "%(hostname, username, pid) + "%(module)s:%(lineno)s [%(levelname)s] %(message)s"
    formats = "%(asctime)-15s %(levelname)s : %(message)s"

    handlerf = logging.FileHandler(logfile)
    handlerf.setLevel(logging.DEBUG)
    handlerf.setFormatter(logging.Formatter(formatf))
    logger.addHandler(handlerf)

    handlers = logging.StreamHandler()
    handlers.setLevel(logging.INFO)
    handlers.setFormatter(logging.Formatter(formats))
    logger.addHandler(handlers)

# config_logger()

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        #logger.error("Ctrl-C pressed.", exc_info=(exc_type, exc_value, exc_traceback))
        #sys.exit(1)
        return

    name = type(exc_value).__name__ if hasattr(type(exc_value), "__name__") else "(unknown)"
    logger.error("Uncaught exception: %s: %s" % (name, exc_value), exc_info=(exc_type, exc_value, exc_traceback))
# handle_exception()

sys.excepthook = handle_exception
