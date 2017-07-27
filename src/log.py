import logging
import logging.config

def setup_custom_logger(name, config):
    logging.config.dictConfig(config)
    logging.info("hi")
  