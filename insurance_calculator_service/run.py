"""
This file allows you to run the app programmatically,
and also enables debugging if this file is run as the main
"""

import sys
from pathlib import Path

import uvicorn

from insurance_calculator_service import options, logger, routes


DEBUGGING = "debugpy" in sys.modules
app = routes.app  # for uvicorn.run


def run(host: str = "localhost") -> None:
    logger.log_section_separator()

    file = Path(__file__)
    uvicorn.run(
        f"{file.stem}:app",
        app_dir=str(file.parent.absolute()),
        host=host,
        port=80,
        reload=options.RELOAD,
        log_level="info",
        log_config=logger.get_config(),
        use_colors=options.DEV_MODE,
    )


if __name__ in ("__mp_main__", "__main__"):
    # if this file is launched directly, this is a sign that it is a dev
    options.DEV_MODE = True

    # if we are not debugging, which requires RELOAD == False,
    # we set the RELOAD to True to simplify the development
    if not DEBUGGING:
        options.RELOAD = True

if __name__ == "__main__":
    run()
