pipeline {
    agent any
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'prod'], description: 'Select environment for deployment')
    }
    
    environment {
        PYTHON_INTERPRETER = '/usr/local/opt/python@3.11/bin/python3.11'
        PYTHON_SCRIPT = 'test.py'
        JSON_FILE = 'trigger.json' // Use the trigger.json file to get the changed values
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        
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
                    def jsonData = readJSON text: jsonContent
                    
                    // Loop through each key-value pair in the JSON data
                    jsonData.each { pipelineName, parameterValue ->
                        // Trigger the pipeline only if the parameter value is found in the changed values
                        if (parameterValue in jsonData.values()) {
                            build job: pipelineName, parameters: [string(name: 'version', value: parameterValue), string(name: 'env', value: params.ENVIRONMENT)]
                        }
                    }
                    
                    // Erase the content of the trigger.json file
                    writeFile file: env.JSON_FILE, text: '{}'
                }
            }
        }
        
        stage('Commit and Push Changes') {
            steps {
                script {
                    // Commit and push changes to the GitHub repository
                    gitAdd = 'git add config.json'
                    gitCommit = 'git commit -m "Update config.json"'
                    gitPush = 'git push origin master' // Modify 'master' to your branch name if needed
                    sh "${gitAdd} && ${gitCommit} && ${gitPush}"
                }
            }
        }
    }
}
