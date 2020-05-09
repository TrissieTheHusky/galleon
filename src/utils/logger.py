#  Copyright (c) 2020 defracted
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
