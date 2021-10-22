from impl.environment import Environment
from impl.logger import Logger
from impl.ServerQueueServiceImpl import ServerQueueServiceImpl
from time import sleep

config = Environment()
logging = Logger.get_logger()


def hello_word(body):
    logging.info("hello word request received")
    return "hello word from service (UUID: %s)" % body


queue = None


def retry(func):
    for i in range(0, 5):
        while True:
            try:
                return func()
            except AMQPConnectionError:
                sleep(3)
                continue
            break


if __name__ == "__main__":
    sleep(5)
    logging.debug("Test start")
    queue = ServerQueueServiceImpl(config.rb_username, config.rb_password, config.rb_hostname, config.rb_port, 'hello_word', hello_word)
