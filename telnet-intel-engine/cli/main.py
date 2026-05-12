from scanner.scanner_pool import run_scan
from features.vectorizer import vectorize
from ml.bayesian import BayesianClassifier

def main():
    targets = ["127.0.0.1"]
    results = run_scan(targets)
    model = BayesianClassifier()

    for r in results:
        r["score"] = model.predict(r["features"])

    print(results)

if __name__ == "__main__":
    main()
