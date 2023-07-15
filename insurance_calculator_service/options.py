"""
Changeable application-wide settings and options
"""

import os

# by default we don't reload, normal production mode
RELOAD: bool = False

# by default we run in production mode
DEV_MODE: bool = False

# by default we log to stdout
LOG_TO_FILE: bool = False

# nice default is inmemory sqlite, user or docker can override this
DB_URL = os.environ.get("DB_URL", "sqlite://:memory:")
