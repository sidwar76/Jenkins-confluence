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
        GITHUB_TOKEN = credentials('9e9656ce-d529-4f73-b93e-5d6e5c923048') // Credential ID of your GitHub token
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
                    // Checkout code from Git repository using the GitHub token
                    git credentialsId: env.GITHUB_TOKEN, url: 'https://github.com/sidwar76/Jenkins-confluence'
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
                    // Configure Git to use the store credential helper globally
                    sh 'git config --global credential.helper store'
                    
                    // Commit and push changes to GitHub using the GitHub token
                    sh "git config --global user.email 'you@example.com'"
                    sh "git config --global user.name 'Your Name'"
                    sh "git add ${FILE_TO_PUSH}"
                    sh "git commit -m 'Update config.json'"
                    sh "git push --set-upstream origin master"
                }
            }
        }
    }
}
