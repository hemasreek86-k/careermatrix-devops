pipeline {
    agent any

    environment {
        ECR_REPO = '<account-id>.dkr.ecr.ap-south-1.amazonaws.com/careermatrix-repo'
        IMAGE_TAG = 'latest'
    }

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/your-username/careermatrix-devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $ECR_REPO:$IMAGE_TAG .'
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin $ECR_REPO
                docker push $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                '''
            }
        }
    }
}
