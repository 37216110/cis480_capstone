"""Shared, leakage-safe helpers for AI4I machine-failure notebooks."""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score

RANDOM_STATE = 42
PREDICTORS = ["Type", "Air temperature [K]", "Process temperature [K]",
              "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"]
NUMERIC_FEATURES = [c for c in PREDICTORS if c != "Type"]
CATEGORICAL_FEATURES = ["Type"]
TARGET = "Machine failure"
FAILURE_FLAGS = ["TWF", "HDF", "PWF", "OSF", "RNF"]


def project_root(start=None):
    """Find project root when launched from project root or a nested notebook folder."""
    start = Path(start or Path.cwd()).resolve()
    for folder in (start, *start.parents):
        if (folder / "data").is_dir() and (folder / "src").is_dir():
            return folder
    raise FileNotFoundError(
        "Cannot find project root containing both data/ and src/. Open the project in VS Code.")


def load_clean_data(root=None, filename="ai4i2020_cleaned.csv"):
    root = Path(root) if root is not None else project_root()
    path = root / "data" / "cleaned" / filename
    if not path.is_file():
        raise FileNotFoundError(
            f"Cleaned dataset missing: {path}. Run the cleaning script first.")
    df = pd.read_csv(path)
    missing = set(PREDICTORS + [TARGET]) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df[PREDICTORS + [TARGET]].isna().any().any():
        raise ValueError("Missing values in predictors or target")
    if not df[TARGET].isin([0, 1]).all():
        raise ValueError("Target must be binary (0/1)")
    if not df["Type"].isin(["L", "M", "H"]).all():
        raise ValueError("Unexpected Type value")
    if set(FAILURE_FLAGS).issubset(df.columns):
        if not df[TARGET].eq(df[FAILURE_FLAGS].max(axis=1)).all():
            raise ValueError(
                "Failure flags disagree with target; run cleaning first")
    return df


def split_data(df, test_size=0.2, random_state=RANDOM_STATE):
    """Shared deterministic stratified split. Never include failure-mode flags."""
    return train_test_split(df[PREDICTORS].copy(), df[TARGET].copy(),
                            test_size=test_size, random_state=random_state, stratify=df[TARGET])


def make_preprocessor(scale_numeric=True):
    """Fit transformations inside a model pipeline, using training folds only."""
    from sklearn.preprocessing import FunctionTransformer
    transformers = [("numeric", StandardScaler() if scale_numeric else "passthrough", NUMERIC_FEATURES),
                    ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES)]
    return ColumnTransformer(transformers)


def make_pipeline(estimator, scale_numeric=True):
    return Pipeline([("preprocessor", make_preprocessor(scale_numeric)), ("classifier", estimator)])


def make_cv(n_splits=5, random_state=RANDOM_STATE):
    return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)


CV_SCORING = {"precision": "precision", "recall": "recall", "f1": "f1",
              "roc_auc": "roc_auc", "average_precision": "average_precision"}


def evaluate_classifier(model, X_test, y_test, threshold=0.5):
    """Return a consistent performance table and predictions for all notebooks."""
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    scores = {
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(y_test, predictions, zero_division=0),
        "Recall": recall_score(y_test, predictions, zero_division=0),
        "F1 Score": f1_score(y_test, predictions, zero_division=0),
        "ROC-AUC": roc_auc_score(y_test, probabilities),
        "Average Precision (PR-AUC)": average_precision_score(y_test, probabilities),
    }
    return pd.DataFrame({"Metric": list(scores), "Score": list(scores.values())}), predictions, probabilities
