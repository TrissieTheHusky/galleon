import logging

import coloredlogs

logger = logging.getLogger('discord')
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

coloredlogs.install(
    level='INFO',
    logger=logger,
    fmt="%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] | %(levelname)s | %(module)s:%(funcName)s:%(lineno)s - %(message)s"
)
