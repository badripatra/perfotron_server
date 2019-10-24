cd "$(dirname "$(realpath "$0")")";
service=`ps -ef|grep JENKINS_HOME|grep -v grep|wc -l`
if [ "$service" = 0 ]
then
    sudo fuser -k 8080/tcp
    sudo yum -y install java-1.8.0-openjdk-devel
    curl --silent --location http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo | sudo tee /etc/yum.repos.d/jenkins.repo
    sudo rpm --import https://jenkins-ci.org/redhat/jenkins-ci.org.key
    sudo yum -y install jenkins
    sudo yum -y install zip
    sudo systemctl start jenkins
    sudo systemctl enable jenkins
    sudo systemctl stop jenkins
    sudo systemctl start jenkins
    sudo yum -y install xorg-x11-server-Xvfb
    sleep 60
else
    echo "Skipping Step : Jenkins Installation  as installer identified a existing Jenkins Setup."
fi