import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGGER_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'all': {
            'format': '%(asctime)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'logger.log'),
            'formatter': 'all',
            'encoding': 'utf8',
            'when': 'D',
            'interval': 1,
            'backupCount': 14,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'all',
        },
    },
    'loggers': {
        'logger': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
