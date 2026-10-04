pipeline {
    agent any

    environment {
        IMAGE_NAME = 'tanay25/flask-login-app'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/tanay25/flask-login-app.git'
            }
        }
        stage('Python Tests') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                python3 -m py_compile app.py
                '''
            }
        }
        stage('Docker Build') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:latest .
                '''
                
            }
        }
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }
        stage('Docker Push') {
            steps {
                sh '''
                docker push $IMAGE_NAME:latest
                '''
            }
        }
        stage('Docker Deploy'){
            steps {
                sh '''
                docker compose down || true
                docker compose up -d --build
                '''
            }
        }
    }
}