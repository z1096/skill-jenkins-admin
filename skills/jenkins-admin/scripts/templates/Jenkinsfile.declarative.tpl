// {{NAME}} pipeline — auto-generated starter
//
// Replace the stage bodies below with your real build/deploy logic.
// Keep the options and post blocks as a baseline; remove what you don't need.
//
// Recommended next steps once stages compile:
//   1. Add parameters (string, choice, git-parameter) in the Jenkins job XML.
//   2. If multiple services share the same shape, factor common helpers out
//      into a shared library or sibling Jenkinsfile and load via 'load' /
//      readTrusted / readYaml.
//   3. Send build notifications (e.g. via a webhook) in post {} blocks.

pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '10'))
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        LC_ALL = 'C.UTF-8'
        LANG   = 'C.UTF-8'
    }

    stages {
        stage('1-Checkout') {
            steps {
                // For 'Pipeline script from SCM' the workspace already has the
                // repository checked out before this Jenkinsfile runs. If you
                // need a different ref, do an explicit checkout step here.
                echo "Pipeline ${env.JOB_NAME} build #${env.BUILD_NUMBER}"
                echo "Branch/tag: ${env.GIT_BRANCH ?: '(not set)'}"
                sh 'git rev-parse HEAD || true'
            }
        }

        stage('2-Build') {
            steps {
                // TODO: replace with the actual build command. Examples:
                //   sh 'make build'
                //   sh 'go build ./...'
                //   sh 'mvn -B -DskipTests package'
                echo 'TODO: build step'
            }
        }

        stage('3-Test') {
            steps {
                // TODO: replace with the actual test command.
                echo 'TODO: test step'
            }
        }

        stage('4-Deploy') {
            when {
                // Disabled by default; flip the expression once a real target
                // is wired (e.g. expression { params.environment == 'test' }).
                expression { return false }
            }
            steps {
                echo 'TODO: deploy step'
            }
        }
    }

    post {
        always {
            echo "Result: ${currentBuild.result ?: 'SUCCESS'} (duration: ${currentBuild.durationString.split('and counting')[0].trim()})"
        }
    }
}
