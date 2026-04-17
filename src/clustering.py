import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder

from src.preprocessing import get_photo_features, PHOTO_COLS, TARGET_COL


def run_clustering(df, output_dir: str):
    print("\n===== CLUSTERING (KMeans k=3) =====")
    X = get_photo_features(df)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)

    # Inertia como métrica de clustering
    inertia = kmeans.inertia_
    print(f"Inercia KMeans: {inertia:.2f}")

    # --- guardar métricas ---
    metrics = {"inertia": round(inertia, 2), "n_clusters": 3}
    with open(f"{output_dir}/clustering_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # --- reducción a 2D con PCA para visualizar ---
    pca = PCA(n_components=2, random_state=42)
    X_2d = pca.fit_transform(X)

    le = LabelEncoder()
    real_labels = le.fit_transform(df[TARGET_COL])

    # Gráfica 1: clusters obtenidos
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    scatter1 = axes[0].scatter(X_2d[:, 0], X_2d[:, 1],
                               c=clusters, cmap="tab10", s=5, alpha=0.6)
    axes[0].set_title("Clusters KMeans (k=3)")
    axes[0].set_xlabel("PC1")
    axes[0].set_ylabel("PC2")
    plt.colorbar(scatter1, ax=axes[0], label="Cluster")

    # Gráfica 2: clases reales
    scatter2 = axes[1].scatter(X_2d[:, 0], X_2d[:, 1],
                               c=real_labels, cmap="tab10", s=5, alpha=0.6)
    axes[1].set_title("Clases reales (SDSS)")
    axes[1].set_xlabel("PC1")
    axes[1].set_ylabel("PC2")
    cbar = plt.colorbar(scatter2, ax=axes[1])
    cbar.set_ticks(range(len(le.classes_)))
    cbar.set_ticklabels(le.classes_)

    plt.suptitle("KMeans vs Clases Reales — PCA 2D", fontsize=13)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/clustering_comparison.png", dpi=150)
    plt.close()
    print(f"Gráfica guardada en {output_dir}/clustering_comparison.png")

    return metrics
