import os
import logging
import sys


accesslog = '-'
errorlog = '-'

import os

workers = int(os.environ.get("GUNICORN_PROCESSES", "1"))
threads = int(os.environ.get("GUNICORN_THREADS", "4"))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "120"))
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8080")

forwarded_allow_ips = "*"
secure_scheme_headers = {"X-Forwarded-Proto": "https"}

logging_level = "INFO"
logging.basicConfig(stream=sys.stdout, level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')
