import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from src.preprocessing import split_regression


def run_regression(df, output_dir: str):
    print("\n===== REGRESIÓN LINEAL (redshift) =====")
    X_train, X_test, y_train, y_test = split_regression(df)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)

    print(f"MSE : {mse:.6f}")
    print(f"R²  : {r2:.4f}")

    # --- guardar métricas ---
    metrics = {"MSE": round(mse, 6), "R2": round(r2, 4)}
    with open(f"{output_dir}/regression_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # --- gráfica: real vs predicho ---
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(y_test, y_pred, alpha=0.3, s=10, color="steelblue")
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax.plot(lims, lims, "r--", linewidth=1.5, label="Ideal")
    ax.set_xlabel("Redshift real")
    ax.set_ylabel("Redshift predicho")
    ax.set_title(f"Regresión Lineal — MSE={mse:.4f}  R²={r2:.4f}")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/regression_scatter.png", dpi=150)
    plt.close()
    print(f"Gráfica guardada en {output_dir}/regression_scatter.png")

    return metrics
