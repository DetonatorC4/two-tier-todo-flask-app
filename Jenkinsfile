@Library("shared") _
pipeline{
    agent {label "dev"};

    stages{
        stage("code fetch"){
            steps{
                script{
                    clone("https://github.com/DetonatorC4/two-tier-todo-flask-app.git", "main")
                }
            }
        }
        stage("trivy fs scan"){
            steps{
                script{
                    trivy_fs()
                }
            }
        }
        stage("build"){
            steps{
                sh "docker build -t todo-app ."
            }
        }
        stage("push to dockerhub"){
            steps{
                script{
                    docker_push("dockerHubCreds", "todo-app")
                }
            }
        }
        stage("run / deploy"){
            steps{
                sh "docker compose up -d --build"
            }
        }
    }

    post{
        success{
            script{
                emailext from: 'aayushd711@gmail.com',
                to: 'aayushdarange29@gmail.com',
                body: 'Build success for todo app',
                subject: 'Build Successful'
            }
        }
        failure{
            script{
                emailext from: 'aayushd711@gmail.com',
                to: 'aayushdarange29@gmail.com',
                body: 'Build failed for todo app',
                subject: 'Build Failed'
            }
        }
    }

}