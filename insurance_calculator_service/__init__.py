__version__ = "0.0.0"
__name__ = "insurance_calculator_service"

from . import logger
from .main import main, run
from .routes import app

logger.setup(__name__)
del logger
