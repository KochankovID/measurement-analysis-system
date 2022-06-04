import tempfile

from dependency_injector.wiring import inject

_grey = "\x1b[38;21m"
_blue = "\u001b[34;1m"
_white = "\u001b[37m"
_green = "\u001b[32m"
_magenta = "\u001b[32m"
_cyan = "\u001b[36m"
_yellow = "\x1b[33;21m"
_red = "\x1b[31;21m"
_bold_red = "\x1b[31;1m"
_reset = "\x1b[0m"


@inject
def get_logger_config(log_file_name: str):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {  # The formatter name, it can be anything that I wish
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s: %(funcName)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",  # How to display dates
            },
            "default_colored": {  # The formatter name, it can be anything that I wish
                "format": f"{_cyan}%(asctime)s{_reset} {_white}-{_reset} {_magenta}%(name)s{_reset} {_white}-{_reset} "
                          f"{_bold_red}%(levelname)s{_reset} {_white}-{_reset} {_blue}%(filename)s: %(funcName)s{_reset} "
                          f"{_white}-{_reset} {_cyan}%(message)s{_reset}",
                "datefmt": "%Y-%m-%d %H:%M:%S",  # How to display dates
            },
            "simple": {  # The formatter name
                "format": "%(message)s",  # As simple as possible!
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "default_colored",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": f"{tempfile.mkdtemp(prefix='vendor.', suffix='.logs')}/{log_file_name}.log",
                "mode": "a",
                "maxBytes": 10485760,
                "backupCount": 5,
            },
        },
        "loggers": {
            "": {"level": "DEBUG", "handlers": ["console", "file"]},
        },
    }
