pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/YOUR-USERNAME/careermatrix-devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t careermatrix .'
            }
        }

        stage('Test Docker Image') {
            steps {
                sh 'docker images'
            }
        }
    }
}
