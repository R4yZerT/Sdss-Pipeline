import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

FEATURE_COLS = ["u", "g", "r", "i", "z", "redshift"]
PHOTO_COLS   = ["u", "g", "r", "i", "z"]
TARGET_COL   = "class"
REDSHIFT_COL = "redshift"


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = FEATURE_COLS + [TARGET_COL]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Columnas faltantes en el dataset: {missing}")
    df = df.dropna(subset=required)
    return df


def encode_labels(df: pd.DataFrame):
    le = LabelEncoder()
    y = le.fit_transform(df[TARGET_COL])
    return y, le


def split_classification(df: pd.DataFrame):
    X = df[FEATURE_COLS].values
    y, le = encode_labels(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    return X_train, X_test, y_train, y_test, le


def split_regression(df: pd.DataFrame):
    X = df[PHOTO_COLS].values
    y = df[REDSHIFT_COL].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42
    )
    return X_train, X_test, y_train, y_test


def get_photo_features(df: pd.DataFrame):
    return df[PHOTO_COLS].values
