import os


class Environment:
    def __init__(self):
        self.db_hostname = os.environ.get('DB_HOSTNAME', '127.0.0.1')
        self.db_username = os.environ.get('DB_USERNAME', 'admin')
        self.db_password = os.environ.get('DB_PASSWORD', 'admin')
        self.db_port = int(float(os.environ.get('DB_PORT'))) if os.environ.get('DB_PORT')else 27017
        self.db_name = os.environ.get('DB_NAME', 'mongo')

        self.rb_username = os.environ.get('RABBITMQ_DEFAULT_USER', 'username')
        self.rb_password = os.environ.get('RABBITMQ_DEFAULT_PASS', 'password')
        self.rb_hostname = os.environ.get('RABBITMQ_HOSTNAME', '127.0.0.1')
        self.rb_port = int(float(os.environ.get('RABBITMQ_POST'))) if os.environ.get('RABBITMQ_POST') else 5672