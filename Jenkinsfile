pipeline {
    agent any

    environment {
        DATABASE_URL = 'postgresql+psycopg://novahr:novahr_password@novahr-postgres:5432/novahr_test'
        SECRET_KEY = 'test-secret-key'
        FLASK_APP = 'run.py'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment') {
            steps {
                sh '''
                    python3 --version
                    pip3 --version
                    git --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate

                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Validate Migrations') {
            steps {
                sh '''
                    . .venv/bin/activate

                    flask db upgrade
                    flask db current
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . .venv/bin/activate

                    pytest -v --junitxml=test-results.xml
                '''
            }
        }
    }

    post {
        always {
            junit(
                allowEmptyResults: true,
                testResults: 'test-results.xml'
            )
        }

        success {
            echo 'NovaHR CI validation: PASSED'
        }

        failure {
            echo 'NovaHR CI validation: FAILED'
        }
    }
}
