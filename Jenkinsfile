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
                    // Checkout code from Git repository
                    git 'https://github.com/sidwar76/Jenkins-confluence'
                }
            }
        }
        
        stage('Execute Python Script') {
            steps {
                script {
                    // Execute Python script to get build data
                    sh "${env.PYTHON_INTERPRETER} ${env.PYTHON_SCRIPT}"
                }
            }
        }
        
        stage('Read and Trigger Pipelines') {
            steps {
                script {
                    // Read JSON file from workspace
                    def jsonContent = readFile(file: env.JSON_FILE)
                    
                    // Parse JSON string manually
                    def slurper = new groovy.json.JsonSlurper()
                    def jsonData = slurper.parseText(jsonContent)
                    
                    // Loop through each key-value pair in the JSON data
                    jsonData.each { pipelineName, parameterValue ->
                        // Trigger the pipeline with the provided parameter value
                        build job: pipelineName, parameters: [string(name: 'version', value: parameterValue)]
                    }
                }
            }
        }
    }
}
