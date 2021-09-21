from ..config.config import Config
from matplotlib import pyplot as plt
import pandas as pd


# Doc2Vec & utility preprocessing modules
from gensim.parsing.preprocessing import preprocess_string
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec

# Classifier
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import recall_score, f1_score, precision_score


class SpamManager:
    def __init__(self):
        # Basic constants configuration
        self.config = Config()
        self.training_set_prefix = "train_"
        self.testing_set_prefix = "test_"

    def initialize(self):
        self.run_question2()

    def get_preprocessed_emails(self, training_emails, testing_emails):
        """Helper method that returns an array containing both the preprocessed email sets"""

        emails = []
        emails += [
            TaggedDocument(
                words=preprocess_string(str(email)),
                tags=[self.training_set_prefix + str(index)],
            )
            for index, email in enumerate(training_emails)
        ]
        emails += [
            TaggedDocument(
                words=preprocess_string(str(email)),
                tags=[self.testing_set_prefix + str(index)],
            )
            for index, email in enumerate(testing_emails)
        ]
        return emails

    def evaluate_classifier(self, predicted_results, actual_results):
        """Calculate and display the precision, recall and f1 classifier metrics"""

        # Calculate each of the scores
        precision = precision_score(actual_results, predicted_results)
        recall = recall_score(actual_results, predicted_results)
        f1 = f1_score(actual_results, predicted_results)

        scores = [precision, recall, f1]

        plt.bar(
            x=[1, 2, 3],
            height=scores,
            tick_label=["Precision", "Recall", "F1"],
        )

        # Display value above each bar
        for index, value in enumerate(scores):
            plt.text(
                index + 1,
                0.5,
                str(round(value, 2)),
                color="white",
                fontweight="bold",
            )

        plt.title("Scores")
        plt.ylabel("Value")
        plt.show()

    def run_question2(self):
        """Create neural network classifier from Doc2Vec model and evaluate"""

        # Read csv
        dataset = pd.read_csv(self.config.spam_csv_path)

        # Create 75-25 train/test split
        (
            training_emails,
            testing_emails,
            training_labels,
            testing_labels,
        ) = train_test_split(
            dataset.email, dataset.label, test_size=0.25, random_state=10
        )

        # Create Doc2Vec model
        model = Doc2Vec(min_count=1, window=10, sample=1e-4, negative=5, workers=2)
        emails = self.get_preprocessed_emails(
            training_emails=training_emails, testing_emails=testing_emails
        )

        # Build vocabulary and train model
        model.build_vocab(emails)
        model.train(emails, total_examples=model.corpus_count, epochs=10)

        # Create neural network classifier
        classifier = MLPClassifier(random_state=1, max_iter=500)
        classifier.fit(
            [
                model[self.training_set_prefix + str(index)]
                for index, email in enumerate(training_emails)
            ],
            training_labels,
        )

        # Evaluate neural network
        self.evaluate_classifier(
            classifier.predict(
                [
                    model[self.testing_set_prefix + str(index)]
                    for index, email in enumerate(testing_emails)
                ]
            ),
            testing_labels,
        )
