# Enable this import to use subscription license verification
# from instance.lz4 import start

import sys
from instance.instanceid import InstanceId

# from log_test.log_test import logmain
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

stdout_logger = logging.StreamHandler(sys.stdout)
stdout_logger.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s'))

handler = logging.FileHandler(
    filename='instance/logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logger.addHandler(stdout_logger)
logger.addHandler(handler)


def main():
    InstanceId.start()


# Use this main() to use subscription license verification
# def main():
#     start()


if __name__ == "__main__":
    main()
