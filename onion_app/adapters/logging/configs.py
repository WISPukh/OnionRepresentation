LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'error': {
            'format': '%(pathname)s\n%(asctime)s LINE NUMBER - %(lineno)d: FUNCTION - %(funcName)s \n %(message)s\n'
        },
        'info': {
            'format': 'INFO:\t\t%(message)s'
        },
    },
    'handlers': {
        'info_handler': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'info',
        },
        'error_handler': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'error',
            'filename': 'errors.log',
            'mode': 'a'
        }
    },
    'loggers': {
        '': {
            'level': 'ERROR',
            'handlers': ['error_handler'],
        },
        'info_logger': {
            'level': 'INFO',
            'handlers': ['info_handler'],
            'propagate': False
        }
    }
}
