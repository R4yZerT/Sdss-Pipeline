"""
Pipeline principal — SDSS Astronomical ML
Institución Universitaria de Envigado — Big Data
"""
import os
import sys

from src.preprocessing import load_data
from src.classification import run_classification
from src.regression import run_regression
from src.clustering import run_clustering
from src.utils import ensure_output_dir, save_summary

DATA_PATH  = os.environ.get("DATA_PATH", "data/sdss_sample.csv")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "outputs")


def main():
    print("=" * 50)
    print("  SDSS ML Pipeline — Big Data IUE")
    print("=" * 50)

    ensure_output_dir(OUTPUT_DIR)

    print(f"\nCargando dataset: {DATA_PATH}")
    df = load_data(DATA_PATH)
    print(f"Filas cargadas: {len(df)}")
    print(f"Columnas: {list(df.columns)}")
    print(f"Distribución de clases:\n{df['class'].value_counts()}")

    clf_metrics  = run_classification(df, OUTPUT_DIR)
    reg_metrics  = run_regression(df, OUTPUT_DIR)
    clust_metrics = run_clustering(df, OUTPUT_DIR)

    save_summary({
        "classification": clf_metrics,
        "regression": reg_metrics,
        "clustering": clust_metrics
    }, OUTPUT_DIR)

    print("\n✓ Pipeline completado exitosamente.")


if __name__ == "__main__":
    main()
