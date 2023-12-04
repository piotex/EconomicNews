FROM jenkins/jenkins:latest

ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
ENV CASC_JENKINS_CONFIG /var/jenkins_home/casc.yaml
ENV JENKINS_ADMIN_ID admin
ENV JENKINS_ADMIN_PASSWORD admin

USER root
RUN apt-get update

USER jenkins
COPY jenkins.plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt
RUN touch ${CASC_JENKINS_CONFIG}
COPY seedjob.groovy /usr/local/seedjob.groovy
COPY jenkins.casc.yaml ${CASC_JENKINS_CONFIG}



