pipeline {
    agent any
    
    stages {
        stage('Instalar Dependencias ML') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                '''
            }
        }
        
        stage('Construir Docker') {
            steps {
                // Aquí ya no fallará el comando 'docker'
                sh 'docker build -t sdss-ml-pipeline .'
            }
        }
    }
}