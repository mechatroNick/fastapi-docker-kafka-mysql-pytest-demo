import os
import logging
import sys

ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")
FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
# DATADOG_TRACING_FORMAT = (
#     "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
#     "[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] "
#     "- %(message)s"
# )


def configure_logging():
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [stdout_handler]
    if ENVIRONMENT == "prod" or ENVIRONMENT == "local":
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    logging.basicConfig(
        level=log_level,
        format=FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )
