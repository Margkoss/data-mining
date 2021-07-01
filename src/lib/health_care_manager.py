import pandas as pd
import inquirer

from ..config.config import Config
from matplotlib import pyplot as plt
from collections import Counter
import math


class HealthCareManager:
    def __init__(self):
        self.config = Config()
        self._choices = ["Analyze data"]
        self._questions = [
            inquirer.List(
                "options",
                message="Which part of the first question",
                choices=self._choices,
            ),
        ]

    def initialize(self):
        """Method that manages what to to in health care manager question"""

        answer = inquirer.prompt(self._questions)

        if answer["options"] == self._choices[0]:
            self.analyze_data()
        else:
            exit(0)

    # To Do -> CLEAN UP
    def analyze_data(self):
        """Reads the data file from config"""

        data = pd.read_csv(self.config.health_care_csv_path)

        # Replace boolean values to be verbose
        data["stroke"] = ["No stroke" if x == 0 else "Had a stroke" for x in data["stroke"]]
        data["hypertension"] = ["No hypertension" if x == 0 else "Had hypertension" for x in data["hypertension"]]
        data["ever_married"] = ["Never married" if x == "No" else "Has Married Before" for x in data["ever_married"]]
        data["heart_disease"] = ["No heart disease" if x == 0 else "Had heart disease" for x in data["heart_disease"]]

        # Create counters for all enumerable data
        data_keys, data_values = [], []
        enumerable_counters = {}
        for key in data.drop(["age", "avg_glucose_level", "bmi", "id"], axis="columns"):

            enumerable_counters[key] = Counter(data[key]).most_common()
            for item in enumerable_counters[key]:
                data_keys.append(item[0])
                data_values.append(item[1])

        # Enumerable Groupings of People
        _, groupings_axes = plt.subplots()
        groupings_axes.barh(data_keys, [(x / len(data)) * 100 for x in data_values])
        groupings_axes.set_title("Percentage of people in enumerable groupings")
        groupings_axes.set_xlabel("Percentage of People")
        groupings_axes.set_ylabel("Enumerable Groupings of People")

        # Scatter plot for age and weight
        _, scatter = plt.subplots()
        im = scatter.scatter(
            data["bmi"],
            data["avg_glucose_level"],
            c=data["age"],
            cmap="Greens",
            edgecolors="black",
            linewidth=1,
            alpha=0.75,
        )

        scatter.set_title("BMI in relation with Average Glucose Level")
        scatter.set_xlabel("BMI")
        scatter.set_ylabel("Average Glucose Level")

        clb = plt.colorbar(im)
        clb.ax.tick_params(labelsize=8)
        clb.ax.set_title("Age", fontsize=8)

        # Enumerable percentages
        # TO DO -> Make size dynamic
        _, pie_axes = plt.subplots(nrows=2, ncols=4)

        for i, item in enumerate(enumerable_counters):
            pie_axes[math.floor(i / 4)][i % 4].pie(
                [x[1] for x in enumerable_counters[item]], labels=[x[0] for x in enumerable_counters[item]]
            )
            pie_axes[math.floor(i / 4)][i % 4].set_title(item)

        plt.show()
