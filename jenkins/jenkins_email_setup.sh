cd "$(dirname "$(realpath "$0")")";
file="/var/lib/jenkins/hudson.plugins.emailext.ExtendedEmailPublisher.xml"
if [ ! -f "$file" ]
then
    sudo cp hudson.plugins.emailext.ExtendedEmailPublisher.xml /var/lib/jenkins/
    sudo chown jenkins:jenkins /var/lib/jenkins/hudson.plugins.emailext.ExtendedEmailPublisher.xml
    sudo cp hudson.tasks.Mailer.xml /var/lib/jenkins/
    sudo chown jenkins:jenkins /var/lib/jenkins/hudson.tasks.Mailer.xml
    sudo cp jenkins.model.JenkinsLocationConfiguration.xml /var/lib/jenkins/
    sudo chown jenkins:jenkins /var/lib/jenkins/jenkins.model.JenkinsLocationConfiguration.xml
    sudo systemctl restart jenkins
else
    echo "Skipping Step : Jenkins email configuration as installer identified a existing Jenkins Setup. "
fi
