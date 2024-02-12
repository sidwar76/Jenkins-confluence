pipeline {
    agent any
    
    environment {
        PYTHON_INTERPRETER = '/usr/local/opt/python@3.11/bin/python3.11'
        PYTHON_SCRIPT = 'test.py'
        JSON_FILE = 'config.json'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    git 'https://github.com/sidwar76/Jenkins-confluence'
                }
            }
        }
        
        stage('Execute Python Script') {
            steps {
                script {
                    sh "${env.PYTHON_INTERPRETER} ${env.PYTHON_SCRIPT}"
                }
            }
        }
        
        stage('Read and Trigger Pipelines') {
            steps {
                script {
                    // Importing the parseJsonFile method from parseJson.groovy
                    def jsonData = load 'parseJson.groovy'
                    
                    jsonData.each { pipelineName, parameterValue ->
                        build job: pipelineName, parameters: [string(name: 'version', value: parameterValue)]
                    }
                }
            }
        }
    }
}
