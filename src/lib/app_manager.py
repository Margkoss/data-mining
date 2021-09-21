import inquirer

from ..config.config import Config
from .health_care_manager import HealthCareManager
from .spam_manager import SpamManager


class AppManager:
    """Class that manages execution context"""

    def __init__(self):

        self._choices = ["Run first question", "Run second question"]

        self._questions = [
            inquirer.List(
                "options",
                message="What do you want to do?",
                choices=self._choices,
            ),
        ]

        self.config = Config()

    def initialize(self):
        """Initializes the application and manages what to do next by asking for user input"""

        answer = inquirer.prompt(self._questions)

        if answer["options"] == self._choices[0]:
            HealthCareManager().initialize()
        else:
            # TO DO -> Add manager for Questions 2
            SpamManager().initialize()
            pass
