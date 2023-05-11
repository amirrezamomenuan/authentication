from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / 'logs'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s -> %(message)s'
        },
    },
    'handlers': {
        'django_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': str(LOG_DIR/'django.log'),
            'formatter': 'simple'
        },
        'otp': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': str(LOG_DIR/'otp.log'),
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['django_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'otp': {
            'handlers': ['otp'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
