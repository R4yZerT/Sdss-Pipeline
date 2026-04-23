pipeline {
    agent any

    stages {
        stage('Limpiar Workspace') {
            steps {
                // Borra todo lo viejo para evitar el error Git 500/128
                deleteDir() 
            }
        }
        stage('Checkout') {
            steps {
                // Descarga el código fresco
                git branch: 'main', url: 'https://github.com/R4yZerT/Sdss-Pipeline.git'
            }
        }
        stage('Construir Docker') {
            steps {
                // Construye la imagen con el nuevo Dockerfile
                sh 'docker build -t sdss-ml-pipeline .'
            }
        }
        stage('Ejecutar Pipeline ML') {
            steps {
                // Corre el contenedor SIN el parámetro -v. 
                // Usará el sdss_sample.csv que el Dockerfile ya metió adentro.
                sh 'docker run --rm sdss-ml-pipeline'
            }
        }
    }
}