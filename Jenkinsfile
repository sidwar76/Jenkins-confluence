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
        GIT_USERNAME = 'sidwar76'     // Your GitHub username
        GIT_TOKEN = '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'  // Your GitHub Personal Access Token (PAT)
        REPO_URL = "https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/sidwar76/Jenkins-confluence"  // Modify with your repository URL
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
                    git url: REPO_URL, credentialsId: 'github-pat'
                }
            }
        }
        
        stage('Execute Python Script') {
            steps {
                script {
                    // Execute Python script to get build data
                    sh "${PYTHON_INTERPRETER} ${PYTHON_SCRIPT}"
                }
            }
        }
        
        stage('Read and Trigger Pipelines') {
            steps {
                script {
                    // Read JSON file from workspace
                    def jsonContent = readFile(file: JSON_FILE)
                    
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
                    writeFile file: JSON_FILE, text: '{}'
                }
            }
        }
        
        stage('Commit and Push Changes') {
            steps {
                script {
                    // Configure Git with the username and email
                    sh 'git config --global user.name "Your Name"'
                    sh 'git config --global user.email "youremail@example.com"'

                    // Initialize Git repository
                    sh 'git init'

                    // Add the file to the repository
                    sh "git add ${FILE_TO_PUSH}"

                    // Commit the changes
                    sh 'git commit -m "Update config.json"'

                    // Set the remote repository URL
                    sh "git remote add origin ${REPO_URL}"

                    // Push the changes to GitHub
                    sh 'git push -u origin master'
                }
            }
        }
    }
}
