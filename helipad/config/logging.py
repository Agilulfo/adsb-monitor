import logging
import logging.handlers
import logging.config


def init_logging():
    config = {
        "version": 1,
        "formatters": {"simple": {"format": "%(levelname)s - %(message)s"}},
        "filters": {},
        "handlers": {
            "to_file": {
                "class": logging.handlers.RotatingFileHandler,
                "filename": "logs.txt",
                "formatter": "simple",
            },
            "to_console": {
                "class": logging.StreamHandler,
                "formatter": "simple",
            },
        },
        "loggers": {
            "__main__": {"handlers": ["to_file"], "level": logging.DEBUG},
            "helipad.handlers": {"handlers": ["to_file"], "level": logging.DEBUG},
            "helipad.streams": {"handlers": ["to_file"], "level": logging.DEBUG},
        },
        "root": {"handlers": ["to_file"]},
    }

    logging.config.dictConfig(config)
