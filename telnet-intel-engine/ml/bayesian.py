import numpy as np

class BayesianClassifier:
    def predict(self, x):
        p27, p28 = 0.4, 0.6
        if x["banner_inetutils"]:
            p28 += 0.2
        return {"2.7": p27, "2.8": p28}
