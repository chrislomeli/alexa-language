import logging
import os

import boto3
from botocore.exceptions import ClientError

from source.model import StorageManager, FlashCard


class LocalStorage(StorageManager):

    def __init__(self, root_directory):
        super().__init__()
        self.root_directory = root_directory
        if not os.path.exists(root_directory):
            os.makedirs(root_directory)

    def check_exists(self):
        file_path = self.flash_card.url
        full_path = os.path.join(self.root_directory, file_path)
        return os.path.exists(full_path)

    def write_audio(self, data: bytes) -> str:
        file_path = self.flash_card.url
        full_path = os.path.join(self.root_directory, file_path)

        dir_name = os.path.dirname(full_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file = open(full_path, 'wb')
        file.write(data)
        file.close()
        self.flash_card.url = full_path
        return full_path

    def read_audio(self) -> (dict, bool):
        file_path = self.flash_card.url
        full_path = os.path.join(self.root_directory, file_path)
        return full_path
