"""
Pruebas básicas del dataset SDSS para validación en Jenkins.
Uso: python -m pytest tests/ -v
"""
import os
import pytest
import pandas as pd

DATA_PATH = os.environ.get("DATA_PATH", "data/sdss_sample.csv")
REQUIRED_COLS = ["u", "g", "r", "i", "z", "redshift", "class"]
EXPECTED_CLASSES = {"STAR", "GALAXY", "QSO"}


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA_PATH)


def test_file_exists():
    assert os.path.isfile(DATA_PATH), f"Dataset no encontrado: {DATA_PATH}"


def test_required_columns(df):
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    assert not missing, f"Columnas faltantes: {missing}"


def test_no_empty_dataset(df):
    assert len(df) > 0, "El dataset está vacío"


def test_no_all_nulls(df):
    for col in REQUIRED_COLS:
        null_pct = df[col].isnull().mean()
        assert null_pct < 1.0, f"Columna '{col}' tiene 100% de nulos"


def test_class_values(df):
    actual = set(df["class"].dropna().unique())
    unexpected = actual - EXPECTED_CLASSES
    assert not unexpected, f"Clases inesperadas en el dataset: {unexpected}"


def test_numeric_features(df):
    for col in ["u", "g", "r", "i", "z", "redshift"]:
        assert pd.api.types.is_numeric_dtype(df[col]), \
            f"Columna '{col}' no es numérica"


def test_minimum_samples_per_class(df):
    counts = df["class"].value_counts()
    for cls, count in counts.items():
        assert count >= 10, f"Clase '{cls}' tiene muy pocas muestras: {count}"
