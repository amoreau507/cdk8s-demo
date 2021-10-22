import logging

class Logger:
    __instance = None
    __logger = None

    def __init__(self):
        if not Logger.__instance:
            Logger.__instance = self
            Logger.__logger = self._create_logger()

    def _create_logger(self):
        logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        return logging.getLogger(__name__)
    
    @staticmethod
    def get_logger():
        if not Logger.__instance:
             Logger()
        return Logger.__logger