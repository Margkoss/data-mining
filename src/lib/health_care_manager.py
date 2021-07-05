import pandas as pd
import numpy as np
import inquirer
import math

from ..config.config import Config
from matplotlib import pyplot as plt
from collections import Counter
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder


class HealthCareManager:
    def __init__(self):
        self.config = Config()
        self._choices = ["Analyze data", "Clean Data"]
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

        elif answer["options"] == self._choices[1]:

            self.clean_data()
        else:
            exit(0)

    # To Do -> CLEAN UP
    def analyze_data(self):
        """Reads the data file from config"""

        data = pd.read_csv(self.config.health_care_csv_path)

        # Replace boolean values to be verbose
        # TO DO -> Do it with pandas replace methods
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
            data["age"],
            data["avg_glucose_level"],
            c=data["bmi"],
            cmap="Greens",
            edgecolors="black",
            linewidth=1,
            alpha=0.75,
        )

        scatter.set_title("Age in relation with Average Glucose Level")
        scatter.set_xlabel("Age")
        scatter.set_ylabel("Average Glucose Level")
        clb = plt.colorbar(im)
        clb.ax.tick_params(labelsize=8)
        clb.ax.set_title("BMI", fontsize=8)

        # Enumerable percentages
        # TO DO -> Make size dynamic
        _, pie_axes = plt.subplots(nrows=2, ncols=4)

        for i, item in enumerate(enumerable_counters):
            pie_axes[math.floor(i / 4)][i % 4].pie(
                [x[1] for x in enumerable_counters[item]], labels=[x[0] for x in enumerable_counters[item]]
            )
            pie_axes[math.floor(i / 4)][i % 4].set_title(item)

        plt.show()

    def clean_data(self):
        """Runs the second question and cleans data"""

        # Replace the unknown values of the smoking columns as nan, so pandas can auto remove
        data = pd.read_csv(self.config.health_care_csv_path, na_values=["Unknown"])

        # Method ONE: Remove columns
        removed_column_method = data.copy()
        removed_column_method.dropna(how="any", axis="columns", inplace=True)

        # Method TWO: Fill all nan values with mean of column
        # Note: Obviously missing data in the "smoking_status" column will not be replaced, as they don't have a mean value
        mean_method = data.copy()
        mean_method["bmi"].fillna(mean_method["bmi"].mean(), inplace=True)

        # Method THREE: Fill all nan values with prediction from linear regression
        train_data = data.copy().dropna(subset=["bmi"], how="any", axis="index").drop("id", axis="columns")

        # Apply label encoding and one hot encoding to categorical data
        train_data.smoking_status = LabelEncoder().fit_transform(train_data.smoking_status)
        train_data.ever_married = train_data.ever_married.replace(["Yes", "No"], [1, 0])
        train_data.gender = LabelEncoder().fit_transform(train_data.gender)
        train_data = pd.get_dummies(data=train_data)

        # Create Linear regression Model
        linear_regression_model = LinearRegression().fit(train_data.drop("bmi", axis="columns"), train_data["bmi"])

        # Apply encoding to output data as well
        lin_reg_tr = data.copy().drop("id", axis="columns")
        lin_reg_tr.smoking_status = LabelEncoder().fit_transform(lin_reg_tr.smoking_status)
        lin_reg_tr.gender = LabelEncoder().fit_transform(lin_reg_tr.gender)
        lin_reg_tr.ever_married = lin_reg_tr.ever_married.replace(["Yes", "No"], [1, 0])
        lin_reg_tr = pd.get_dummies(data=lin_reg_tr)

        linear_reg_method = data.copy()

        # For each element in bmi check if it is np.nan and predict value if it is
        for i in lin_reg_tr.index:
            linear_reg_method.at[i, "bmi"] = (
                linear_regression_model.predict(np.array([lin_reg_tr.loc[i].drop("bmi", axis="index")]))[0]
                if np.isnan(lin_reg_tr.at[i, "bmi"])
                else lin_reg_tr.at[i, "bmi"]
            )

        # Method FOUR: Fill all nan values with prediction from KNN
