import logging
from multiprocessing import get_logger
formatter = logging.Formatter('[%(levelname)s/%(processName)s] %(message)s')
shandler = logging.StreamHandler()
shandler.setFormatter(formatter)
logger = get_logger()
logger.addHandler(shandler)