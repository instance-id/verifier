# Enable this import to use subscription license verification
# from instance.lz4 import start

from instance.instanceid import InstanceId

# from log_test.log_test import logmain
import logging

# <editor-fold desc="Logging definitions">
from colorlog import ColoredFormatter

log = logging.getLogger(__name__)
LOG_LEVEL = logging.INFO
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log.setLevel(LOG_LEVEL)
log.addHandler(stream)
# </editor-fold>


def main():
    InstanceId.start()


# Use this main() to use subscription license verification
# def main():
#     start()


if __name__ == "__main__":
    main()
