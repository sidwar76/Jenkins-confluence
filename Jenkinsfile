pipeline {
    agent any
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'prod'], description: 'Select environment for deployment')
    }
    
    environment {
        PYTHON_INTERPRETER = '/usr/local/opt/python@3.11/bin/python3.11'
        PYTHON_SCRIPT = 'test.py'
        JSON_FILE = 'trigger.json' // Use the trigger.json file to get the changed values
        FILE_TO_PUSH = 'config.json'  // The file you want to push
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
                    // Checkout code from Git repository using SSH key authentication
                    git url: 'git@github.com:sidwar76/Jenkins-confluence.git'
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
                    // Check if there are any changes in the FILE_TO_PUSH
                    def changes = sh(script: "git diff --exit-code ${FILE_TO_PUSH}", returnStatus: true)
                    
                    // If there are changes, stage and commit
                    if (changes == 1) {
                        sh "git add ${FILE_TO_PUSH}"
                        sh "git commit -m 'Update ${FILE_TO_PUSH}'"
                        sh "git push --set-upstream origin master"
                    } else {
                        echo "No changes detected in ${FILE_TO_PUSH}. Skipping commit."
                    }
                }
            }
        }
    }
}
