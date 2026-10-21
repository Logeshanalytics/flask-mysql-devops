pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

       stage('Test') {
        steps {
            sh '''
            docker run --rm \
              -e PYTHONPATH=/app \
              -v "$WORKSPACE:/app" \
              -w /app \
              python:3.12-slim \
              sh -c "pip install --no-cache-dir -r requirements.txt && python -m pytest -q"
        '''
    }
}

        stage('Build Image') {
            steps {
                sh '''
                    docker build -t flask-mysql-app:${BUILD_NUMBER} .
                    docker tag flask-mysql-app:${BUILD_NUMBER} flask-mysql-app:latest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    test -f /opt/flask-mysql-devops/.env

                    docker compose \
                      --project-directory "$WORKSPACE" \
                      --env-file /opt/flask-mysql-devops/.env \
                      -f "$WORKSPACE/compose.yaml" \
                      up -d --build
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    for i in $(seq 1 30); do
                        if curl --fail --silent http://localhost/health; then
                            echo "Deployment successful"
                            exit 0
                        fi
                        sleep 2
                    done

                    echo "Health check failed"
                    docker compose \
                      --project-directory "$WORKSPACE" \
                      --env-file /opt/flask-mysql-devops/.env \
                      -f "$WORKSPACE/compose.yaml" logs
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Review the stage logs.'
        }
    }
}
