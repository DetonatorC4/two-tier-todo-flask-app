pipeline{
    agent any;

    stages{
        stage("code fetch"){
            steps{
                git url: "https://github.com/DetonatorC4/two-tier-todo-flask-app.git", branch: "main"
            }
        }
        stage("build"){
            steps{
                sh "docker build -t todo-app ."
            }
        }
        stage("push to dockerhub"){
            steps{
                withCredentials([usernamePassword(credentialsId:"dockerHubCreds", passwordVariable: "PASSWORD", usernameVariable: "USERNAME")]) {
                    sh "docker login -u ${env.USERNAME} -p ${env.PASSWORD}"
                    sh "docker tag todo-app ${env.USERNAME}/todo-app:latest"
                    sh "docker push ${env.USERNAME}/todo-app:latest"
                }
            }
        }
        stage("run / deploy"){
            steps{
                sh "docker compose up -d --build"
            }
        }
    }
}