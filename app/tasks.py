import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(*args):
    logger.info('in handler')
    logger.info(args)
    print(args)