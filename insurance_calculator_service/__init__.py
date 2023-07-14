__version__ = "0.0.0"
__name__ = "insurance_calculator_service"

from . import logger
from .cli import main
from .routes import app
from .run import run

logger.setup(__name__)
del logger
