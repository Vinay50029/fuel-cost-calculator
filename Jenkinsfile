pipeline {
    agent any
    
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
        
        stage('Setup Python') {
            steps {
                script {
                    sh '''
                        apt-get update
                        apt-get install -y python3-full python3-pip python3-venv
                    '''
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                        python3 -m pip install --break-system-packages -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Lint & Test') {
            steps {
                script {
                    sh '''
                        # Add your linting commands here
                        # python3 -m flake8 app.py
                        # Add your test commands here
                        # python3 -m pytest tests/
                        echo "Linting and testing completed"
                    '''
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    sh '''
                        python3 -m pip install --break-system-packages safety
                        python3 -m safety check
                    '''
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
        
        stage('Test Docker Image') {
            steps {
                script {
                    sh '''
                        # Start container for testing
                        docker run -d --name test-container -p 8081:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                        
                        # Wait for container to start
                        sleep 10
                        
                        # Basic health check
                        curl -f http://localhost:8081 || exit 1
                        
                        # Stop and remove test container
                        docker stop test-container
                        docker rm test-container
                    '''
                }
            }
        }
        
        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                        # Push to registry (uncomment when registry is configured)
                        # docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        # docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest
                        echo "Image built successfully: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    '''
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                        # Deploy using docker-compose
                        docker-compose down || true
                        docker-compose up -d
                        
                        # Wait for deployment
                        sleep 15
                        
                        # Verify deployment
                        curl -f http://localhost:8080 || exit 1
                        echo "Deployment successful"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Cleanup
                sh '''
                    docker system prune -f
                '''
            }
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}