import logging
import logging.config


__logger = None


def init_app(app):
    logging.config.dictConfig(app.config['LOGGING'])

    global __logger
    __logger = logging.getLogger(app.config['API_NAME'])


def error(msg, *args, **kwargs):
    __logger.error(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    __logger.exception(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    __logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    __logger.info(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    __logger.warning(msg, *args, **kwargs)
