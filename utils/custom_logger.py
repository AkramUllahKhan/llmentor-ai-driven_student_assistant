import logging

FMT = "{asctime} [{levelname:^9}] : {message}"  # Format for logging messages
FORMATS = {
    logging.DEBUG: FMT,
    logging.INFO: f"\33[33m{FMT}\33[0m",
    logging.WARNING: "\u001b[46;1m{asctime} [  TIME  ] : {message} \u001b[0m",
    logging.ERROR: f"\33[31m{FMT}\33[0m",
    logging.CRITICAL: f"\u001b[41;1m {FMT}\33[0m",
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style='{')
        return formatter.format(record)

handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter())

# Disable logging for all other loggers
logging.basicConfig(level=logging.CRITICAL, handlers=[handler])

# Configure your specific logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(handler)
log.propagate = False  # Disable propagation to avoid duplication

# Example usage
# log.debug("Hello World!")
# log.info("Hello World!")
# log.warning("Hello World!")
# log.error("Hello World!")
# log.critical("Hello World!")
