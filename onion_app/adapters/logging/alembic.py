def get_logging_config(log_level, sa_logs):
    fmt = '%(asctime)s.%(msecs)03d [%(levelname)s]|[%(name)s]: %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'

    config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': fmt,
                'datefmt': datefmt,
            },
            'json': {
                'format': fmt,
                'datefmt': datefmt,
                'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
            },
        },
        'handlers': {
            'default': {
                'level': log_level,
                'formatter': 'json',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': log_level,
                'propagate': False
            },
            'alembic': {
                'handlers': ['default'],
                'level': log_level,
                'propagate': False
            },
        }
    }

    if sa_logs:
        config['loggers']['sqlalchemy'] = {
            'handlers': ['default'],
            'level': log_level,
            'propagate': False
        }

    return config
