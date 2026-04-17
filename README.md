# SDSS ML Pipeline — Big Data IUE

Pipeline completo de Machine Learning sobre datos astronómicos SDSS.
Incluye clasificación (KNN), regresión lineal y clustering (KMeans).

---

## Estructura del proyecto

```
sdss_pipeline/
├── data/
│   └── sdss_sample.csv        ← Dataset (agregar manualmente)
├── src/
│   ├── preprocessing.py       ← Carga y división de datos
│   ├── classification.py      ← KNN k=5
│   ├── regression.py          ← Regresión lineal (redshift)
│   ├── clustering.py          ← KMeans k=3
│   └── utils.py               ← Utilidades (carpetas, resumen)
├── tests/
│   └── test_dataset.py        ← Pruebas básicas con pytest
├── outputs/                   ← Métricas y gráficas generadas
├── main.py                    ← Script principal
├── requirements.txt
├── Dockerfile
└── Jenkinsfile
```

---

## Ejecución local

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Copiar el dataset
cp /ruta/a/sdss_sample.csv data/

# 3. Ejecutar
python main.py

# 4. Correr pruebas
pip install pytest
pytest tests/ -v
```

---

## Ejecución con Docker

```bash
# 1. Construir imagen
docker build -t sdss-ml-pipeline .

# 2. Ejecutar montando el dataset y la carpeta de salida
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  sdss-ml-pipeline
```

Los resultados quedan en `outputs/` del host.

---

## Outputs generados

| Archivo                        | Descripción                         |
|-------------------------------|-------------------------------------|
| `confusion_matrix.png`        | Matriz de confusión KNN             |
| `classification_metrics.json` | Accuracy + matriz en JSON           |
| `classification_report.txt`   | Reporte completo por clase          |
| `regression_scatter.png`      | Scatter real vs predicho            |
| `regression_metrics.json`     | MSE y R²                            |
| `clustering_comparison.png`   | KMeans vs clases reales (PCA 2D)    |
| `clustering_metrics.json`     | Inercia del modelo                  |
| `summary.json`                | Resumen global de todas las métricas|
| `pipeline.log`                | Log completo de ejecución           |
| `test_results.log`            | Resultados de pytest                |

---

## Jenkins

Importar el repositorio en Jenkins (Pipeline from SCM).
El `Jenkinsfile` define 5 etapas automáticas:
1. Checkout
2. Instalar dependencias
3. Pruebas del dataset (pytest)
4. Ejecutar pipeline ML
5. Archivar artefactos
