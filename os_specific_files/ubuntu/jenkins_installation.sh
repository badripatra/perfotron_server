cd "$(dirname "$(realpath "$0")")";
service=`ps -ef|grep JENKINS_HOME|grep -v grep|wc -l`
if [ "$service" = 0 ]
then
    sudo fuser -k 8080/tcp
	sudo add-apt-repository -y ppa:openjdk-r/ppa
	sudo apt-get update
	sudo apt-get -y install openjdk-8-jdk
	wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | sudo apt-key add -
	echo deb https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list
	sudo apt-get update
	sudo apt-get -y install jenkins
	sudo apt -y install zip
	sudo systemctl start jenkins
	sudo systemctl stop jenkins
	sudo systemctl start jenkins
	sudo apt-get -y install xvfb
else
    echo "Skipping Step : Jenkins Installation  as installer identified a existing Jenkins Setup."
fi
