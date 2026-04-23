pipeline {
    /* Utilizamos un agente de Docker para asegurar que el entorno 
       tenga Python 3.11 instalado, independientemente de la configuración del host.
    */
    agent {
        docker { 
            image 'python:3.11-slim' 
            args  '-u root' // Asegura permisos para crear carpetas y escribir logs
        }
    }

    environment {
        IMAGE_NAME = "sdss-ml-pipeline"
        DATA_PATH  = "data/sdss_sample.csv"
        OUTPUT_DIR = "outputs"
    }

    stages {
        // ── 1. CHECKOUT ─────────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo '==> Sincronizando código fuente...'
                checkout scm
            }
        }

        // ── 2. INSTALACIÓN ──────────────────────────────────────────
        stage('Instalar dependencias') {
            steps {
                echo '==> Instalando librerías de Ciencia de Datos...'
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                '''
            }
        }

        // ── 3. PRUEBAS ──────────────────────────────────────────────
        stage('Pruebas del dataset') {
            steps {
                echo '==> Validando integridad de los datos astronómicos...'
                sh 'pytest tests/ -v > test_results.log'
            }
        }

        // ── 4. EJECUCIÓN ML ─────────────────────────────────────────
        stage('Ejecutar pipeline ML') {
            steps {
                echo '==> Iniciando entrenamiento y evaluación de modelos...'
                // Ejecuta el orquestador principal que genera las gráficas y JSONs
                sh 'python main.py'
            }
        }

        // ── 5. ARTEFACTOS ───────────────────────────────────────────
        stage('Almacenar artefactos') {
            steps {
                echo '==> Archivando métricas y visualizaciones...'
                // Guarda todos los archivos generados en la carpeta outputs
                archiveArtifacts artifacts: "${OUTPUT_DIR}/*.*, *.log", allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo '==> Limpiando espacio de trabajo...'
            cleanWs()
        }
        success {
            echo '✓ El pipeline finalizó exitosamente. Artefactos listos.'
        }
        failure {
            echo '✗ El pipeline falló. Revisar logs de la etapa afectada.'
        }
    }
}