pipeline {
    agent any 

    environment {
        IMAGE_NAME = "sdss-ml-pipeline"
        DATA_PATH  = "data/sdss_sample.csv"
        OUTPUT_DIR = "outputs"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '==> Sincronizando código desde GitHub...'
                checkout scm
            }
        }

        stage('Preparar Contenedor') {
            steps {
                echo '==> Construyendo la imagen de Docker...'
                // Construimos la imagen usando el Dockerfile del repo
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Ejecutar Pipeline ML') {
            steps {
                echo '==> Corriendo modelos dentro del contenedor...'
                /* Ejecutamos el contenedor mapeando las carpetas locales.
                   Esto generará los archivos en outputs/ */
                sh """
                    docker run --rm \
                    -v \$(pwd)/data:/app/data \
                    -v \$(pwd)/outputs:/app/outputs \
                    ${IMAGE_NAME}
                """
            }
        }

        stage('Almacenar Artefactos') {
            steps {
                echo '==> Archivando resultados para la entrega...'
                // Guardamos las métricas y la matriz de confusión
                archiveArtifacts artifacts: "${OUTPUT_DIR}/*.png, ${OUTPUT_DIR}/*.json", allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo '✓ ¡Proyecto completado! Revisa la sección de Artefactos.'
        }
        failure {
            echo '✗ Falló la ejecución. Revisa los logs de Docker.'
        }
    }
}