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
        REPO_URL = 'https://github.com/sidwar76/Jenkins-confluence' // Repository URL
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
                    // Configure Git to use the store credential helper globally
                    sh 'git config --global credential.helper store'
                    
                    // Checkout code from Git repository
                    git url: env.REPO_URL
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
                    // Commit and push changes to GitHub
                    withCredentials([usernamePassword(credentialsId: 'b7a323b4-29ef-4de1-8a71-ed9869d05538', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        sh 'git config --global user.email "you@example.com"'
                        sh 'git config --global user.name "Your Name"'
                        sh "git add ${FILE_TO_PUSH}"
                        sh 'git commit -m "Update config.json"'
                        sh 'git push --set-upstream origin master'  // Modify 'master' to your branch name if needed
                    }
                }
            }
        }
    }
}
