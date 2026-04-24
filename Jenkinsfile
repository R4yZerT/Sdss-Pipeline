pipeline {
    agent any
    
    stages {
        stage('Construir Imagen de Entrenamiento') {
            steps {
                // El Dockerfile ya contiene las instrucciones para instalar Python y las librerías [cite: 1, 2, 3]
                // Esto crea la imagen con el nombre 'sdss-ml-pipeline' 
                sh 'docker build -t sdss-ml-pipeline .'
            }
        }
        
        stage('Ejecutar Entrenamiento IA') {
            steps {
                // Ejecutamos el contenedor basado en la imagen creada.
                // Como la imagen 'bullseye' ya es completa[cite: 2], el comando 'python main.py' funcionará aquí adentro.
                sh 'docker run --rm sdss-ml-pipeline'
            }
        }
    }
}