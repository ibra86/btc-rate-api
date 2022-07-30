import csv
import os
from abc import ABC, abstractmethod

from src.config.config import CONFIG

config_db = CONFIG.get_config('db')


class Registry(ABC):
    @abstractmethod
    def add(self, *args, **kwargs):
        pass


class EmailRegistry:

    def __init__(self):
        self.emails = []
        self.read_emails()

    @property
    def file_path(self):
        config = config_db.get('csv')
        f_path = os.path.join(config['dir_path'], config['file_name'])
        return f_path

    def read_emails(self):
        if not os.path.exists(self.file_path):
            dir_path = config_db.get('csv')['dir_path']
            os.makedirs(dir_path, exist_ok=True)
            open(self.file_path, 'w+').close()

        with open(self.file_path, 'r') as f:
            reader = csv.reader(f)
            for r in reader:
                self.emails.append(','.join(r))

    def write_emails(self, email):
        with open(self.file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([email])

    def add(self, email):
        self.emails.append(email)
        self.write_emails(email)
