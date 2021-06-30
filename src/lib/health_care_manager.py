from ..config.config import Config
from csv import reader


class HealthCareManager:
    def __init__(self):
        self.config = Config()

    def initialize(self):
        """Method that manages what to to in health care manager question"""

        pass

    def read_file(self):

        """Reads the data file from config"""

        try:
            with open(self.config.health_care_csv_path, "r") as read_obj:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    print(row)
        except Exception as e:
            print("File was not found, and therefore not read")
            exit(-1)
