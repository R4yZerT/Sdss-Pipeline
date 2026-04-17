import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from src.preprocessing import split_classification


def run_classification(df, output_dir: str):
    print("\n===== CLASIFICACIÓN (KNN k=5) =====")
    X_train, X_test, y_train, y_test, le = split_classification(df)

    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    cm  = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=le.classes_)

    print(f"Accuracy: {acc:.4f}")
    print("Matriz de confusión:\n", cm)
    print("Reporte completo:\n", report)

    # --- guardar métricas ---
    metrics = {
        "accuracy": round(acc, 4),
        "confusion_matrix": cm.tolist(),
        "classes": list(le.classes_)
    }
    with open(f"{output_dir}/classification_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # --- guardar reporte de texto ---
    with open(f"{output_dir}/classification_report.txt", "w") as f:
        f.write(f"Accuracy: {acc:.4f}\n\n")
        f.write(report)

    # --- gráfica: matriz de confusión ---
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=le.classes_, yticklabels=le.classes_, ax=ax)
    ax.set_xlabel("Predicho")
    ax.set_ylabel("Real")
    ax.set_title("Matriz de Confusión — KNN (k=5)")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/confusion_matrix.png", dpi=150)
    plt.close()
    print(f"Gráfica guardada en {output_dir}/confusion_matrix.png")

    return metrics
