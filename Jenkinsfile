pipeline {
    agent any
    stages {
        stage('Checking out of Github'){
            steps{
                echo "Fetching latest changes from master on github.."
                git 'https://github.com/adimitrova/FunProjects.git'
            }
        }
        stage('Running shell script from git repo'){
            steps{
                echo "running scripts.."
                sh label: 'color test', script: 'bash_scripts/testing_colors.sh'
            }
        }
        stage('Deploy'){
            steps{
                echo "deploying to cloud platform.."
                echo "deployment done."
            }
        }
    }
}