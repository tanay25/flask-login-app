```groovy
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'tanay25/flask-login-app'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/tanay25/flask-login-app.git'
            }
        }

        stage('Python Tests') {
            steps {
                sh '''
                    set -e

                    python3 -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt

                    python3 -m py_compile app.py

                    echo "Python tests completed successfully"
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -e

                    docker build -t ${IMAGE_NAME}:latest .

                    echo "Docker image built successfully"
                    docker images | grep flask-login-app
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        set -e

                        echo "$DOCKER_PASSWORD" | \
                            docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Docker Push') {
            steps {
                sh '''
                    set -e

                    docker push ${IMAGE_NAME}:latest

                    echo "Docker image pushed successfully"
                '''
            }
        }

        stage('Docker Deploy') {
            steps {
                sh '''
                    set -e

                    docker compose down || true
                    docker compose up -d --build

                    echo "Application deployed successfully"
                    docker compose ps
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs above.'
        }
    }
}
```
