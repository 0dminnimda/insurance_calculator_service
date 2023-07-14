from . import logger
from .__metadata__ import __name__, __version__
from .main import main, run
from .routes import app

logger.setup(__name__)
del logger
