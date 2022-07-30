import csv
import os
from abc import ABC, abstractmethod


class Registry(ABC):
    @abstractmethod
    def add(self, email):
        pass


class EmailRegistry:
    # TODO: add to config
    DIR_PATH = 'src/db'
    F_NAME = 'email_registry.csv'

    def __init__(self):
        self.f_path = os.path.join(self.DIR_PATH, self.F_NAME)
        self.emails = []
        self.read_emails()

    def read_emails(self):
        if not os.path.exists(self.f_path):
            os.makedirs(self.DIR_PATH, exist_ok=True)
            open(self.f_path, 'w+').close()

        with open(self.f_path, 'r') as f:
            reader = csv.reader(f)
            for r in reader:
                self.emails.append(','.join(r))

    def write_emails(self, email):
        with open(self.f_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([email])

    def add(self, email):
        self.emails.append(email)
        self.write_emails(email)
