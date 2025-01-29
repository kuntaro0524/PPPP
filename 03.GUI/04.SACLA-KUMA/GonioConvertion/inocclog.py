import time
import sys
import getpass
import logging
import os
import platform

# to prevent error
logging.basicConfig()

# Singleton object
logger = logging.getLogger("inocc")
logger.setLevel(logging.DEBUG)

debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception
log = logger.log


def config(logdir, stream=sys.stdout):
    logging.root.handlers = [] # clear basic config
    logger.handlers = []

    date = time.strftime("%Y%m%d")
    hostname = platform.node()
    hostname = hostname[:hostname.find(".")]
    username = getpass.getuser()
    pid = os.getpid()

    logfile = os.path.join(logdir, "inocc_%s.log"%(getpass.getuser()))
    formatf = "%(asctime)-15s " + " %s : %s : %d : "%(hostname, username, pid) + "%(module)s:%(lineno)s [%(levelname)s] %(message)s"
    formats = "%(asctime)-15s %(levelname)s : %(message)s"

    handlerf = logging.FileHandler(logfile)
    handlerf.setLevel(logging.DEBUG)
    handlerf.setFormatter(logging.Formatter(formatf))
    logger.addHandler(handlerf)

    handlers = logging.StreamHandler(stream)
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
