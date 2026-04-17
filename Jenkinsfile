pipeline {
    agent any

    environment {
        IMAGE_NAME = "sdss-ml-pipeline"
        DATA_PATH  = "data/sdss_sample.csv"
        OUTPUT_DIR = "outputs"
    }

    stages {

        // ── 1. Checkout ────────────────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo '==> Clonando repositorio...'
                checkout scm
            }
        }

        // ── 2. Instalación de dependencias ─────────────────────────────────
        stage('Instalar dependencias') {
            steps {
                echo '==> Instalando dependencias Python...'
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                '''
            }
        }

        // ── 3. Pruebas básicas del dataset ─────────────────────────────────
        stage('Pruebas del dataset') {
            steps {
                echo '==> Ejecutando pruebas con pytest...'
                sh '''
                    . .venv/bin/activate
                    pytest tests/ -v --tb=short 2>&1 | tee outputs/test_results.log
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'outputs/test_results.log',
                                     allowEmptyArchive: true
                }
            }
        }

        // ── 4. Ejecución del pipeline principal ────────────────────────────
        stage('Ejecutar pipeline ML') {
            steps {
                echo '==> Ejecutando main.py...'
                sh '''
                    mkdir -p outputs
                    . .venv/bin/activate
                    python main.py 2>&1 | tee outputs/pipeline.log
                '''
            }
        }

        // ── 5. Artefactos ──────────────────────────────────────────────────
        stage('Almacenar artefactos') {
            steps {
                echo '==> Archivando métricas y gráficas...'
                archiveArtifacts artifacts: 'outputs/**/*',
                                 fingerprint: true,
                                 allowEmptyArchive: false
            }
        }
    }

    post {
        success {
            echo '✓ Pipeline completado exitosamente.'
        }
        failure {
            echo '✗ El pipeline falló. Revisar outputs/pipeline.log'
        }
        always {
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true,
                    patterns: [[pattern: '.venv/**', type: 'INCLUDE']])
        }
    }
}
