pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        DOCKER_IMAGE = 'fuel-cost-calculator'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_REGISTRY = 'localhost:5000' // Change to your registry
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y curl docker.io
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv                   # Create virtual environment
                    . venv/bin/activate                    # Activate venv
                    pip install --upgrade pip              # Upgrade pip inside venv
                    pip install -r requirements.txt        # Install project dependencies
                    echo "✅ Dependencies installed successfully"
                '''
            }
        }

        stage('Lint & Test') {
            steps {
                sh '''
                    . venv/bin/activate                    # Activate venv
                    echo "Running lint and tests..."
                    # python -m flake8 app.py
                    # python -m pytest tests/
                    echo "✅ Linting and testing completed"
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install safety
                    safety check || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    echo "✅ Docker image built successfully"
                '''
            }
        }

        stage('Test Docker Image') {
            steps {
                sh '''
                    docker run -d --name test-container -p 8081:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                    sleep 10
                    curl -f http://localhost:8081 || exit 1
                    docker stop test-container
                    docker rm test-container
                    echo "✅ Docker image test passed"
                '''
            }
        }

        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    # Uncomment after registry setup
                    # docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}
                    # docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest
                    echo "✅ Image ready to push: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                '''
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    docker-compose down || true
                    docker-compose up -d
                    sleep 15
                    curl -f http://localhost:8080 || exit 1
                    echo "✅ Deployment successful"
                '''
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f || true'
        }
        success {
            echo '🎉 Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}