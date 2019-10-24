cd "$(dirname "$(realpath "$0")")";

file="/var/lib/jenkins/jobs/sample-job/config.xml"
if [ ! -f "$file" ]
then
    sudo wget http://mirrors.ocf.berkeley.edu/apache//jmeter/binaries/apache-jmeter-5.1.1.tgz
    sudo tar -xvf apache-jmeter-5.1.1.tgz
    sudo mkdir /var/lib/jenkins/jobs/sample-job
    sudo cp config.xml /var/lib/jenkins/jobs/sample-job/
    sudo chown -R jenkins:jenkins /var/lib/jenkins/jobs/sample-job/
    sudo systemctl restart jenkins
    sudo cp -R apache-jmeter-5.1.1 /var/lib/jenkins/
    sudo chown -R jenkins:jenkins /var/lib/jenkins/apache-jmeter-5.1.1
    sudo cp actual_demo_jmeter_script.jmx /var/lib/jenkins/
    sudo cp Config.cfg /var/lib/jenkins/
    sudo cp generate_report.py /var/lib/jenkins/
    sudo cp Email_Content_template.html /var/lib/jenkins/
    sudo chown -R jenkins:jenkins /var/lib/jenkins/
    sudo mkdir -p /var/lib/jenkins/results/
    sudo chmod -R 777 /var/lib/jenkins/results/
    sudo pip install numpy==1.15.1
    sudo pip install statistics
    sudo pip install pandas==0.22.0
else
    echo "Skipping Step : Jenkins JOb Setup as installer identified a existing Jenkins Setup. "
fi

