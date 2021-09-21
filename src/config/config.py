import os
from pathlib import Path


class Config:
    """Global app configuration"""

    def __init__(self):
        self.health_care_csv_path = os.path.join(
            Path(__file__).parent, '..', "assets", "healthcare-dataset-stroke-data", "healthcare-dataset-stroke-data.csv"
        )
        self.spam_csv_path = os.path.join(
            Path(
                __file__).parent, '..', "assets", "spam_or_not_spam", "spam_or_not_spam.csv"
        )
        self.db_connection_uri = ""
