pipeline {
    agent any
    
    environment {
        PYTHON_INTERPRETER = '/usr/local/opt/python@3.11/bin/python3.11'
        PYTHON_SCRIPT = 'test.py'
        JSON_FILE = 'config.json'
        TRIGGER_JSON_FILE = 'trigger.json'
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
                    // Read JSON file contents
                    def jsonContent = readFile(env.TRIGGER_JSON_FILE).trim()
                    
                    // Parse JSON data
                    def jsonData = parseJsonText(jsonContent)
                    
                    // Check if jsonData is null or empty
                    if (jsonData.isEmpty()) {
                        error "Failed to parse JSON data. Check the JSON file content."
                    }
                    
                    // Print out the parsed JSON data for debugging
                    echo "Parsed JSON Data: ${jsonData}"
                    
                    // Iterate over the parsed JSON data
                    jsonData.each { jobName, parameterValue ->
                        // Print out each pipeline name and parameter value for debugging
                        echo "Triggering job: ${jobName} with parameter: ${parameterValue}"
                        
                        // Trigger the job
                        build job: jobName, parameters: [string(name: 'version', value: parameterValue)]
                    }
                }
            }
        }
    }
}
