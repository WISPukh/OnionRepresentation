from .configs import LOGGING_CONFIG


def get_logging_config(log_level, sa_logs):
    config = LOGGING_CONFIG

    if sa_logs:
        config['loggers']['sqlalchemy'] = {
            'handlers': ['error_handler'],
            'level': log_level,
            'propagate': False
        }

    return config
