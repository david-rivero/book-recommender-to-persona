from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


class TrainerTemplate:
    def __init__(self):
        self.model = LogisticRegression()

    def train_model(self, dataframe, target, test_size=0.4):
        data_train, data_test, target_train, target_test = train_test_split(
            dataframe, target, test_size=test_size)
        self.model.fit(data_train, target_train)

    def predict(self, input_data):
        return self.model.predict(input_data)
